from django.db import transaction
from typing import List, Tuple

from trips.models import Route, Location, Waypoint
from trips.services import RoutingService
from core.constants import PICKUP_DROPOFF_TIME, FUEL_STOP_TIME


class RouteOrchestrator:
    
    @staticmethod
    def _get_api_data(waypoints: List[Tuple[float, float]]) -> Tuple[float, float, List[dict], List]:
        api_response = RoutingService.get_route_from_api(waypoints=waypoints)
        
        if "features" not in api_response or not api_response["features"]:
            raise ValueError(f"Routing API failed: {api_response}")

        feature = api_response['features'][0]
        properties = feature['properties']
        
        return (
            properties['distance'],
            properties['time'],
            properties['legs'][0]['steps'],
            feature["geometry"]["coordinates"]
        )

    @staticmethod
    def _calculate_service_time(required_stops: List[dict]) -> int:
        pickup_dropoff_time = 2 * PICKUP_DROPOFF_TIME * 60
        fuel_stop_time = len([s for s in required_stops if s['type'] == 'fuel']) * FUEL_STOP_TIME * 60
        return pickup_dropoff_time + fuel_stop_time

    @staticmethod
    def _create_intermediate_locations(required_stops: List[dict]) -> List[Tuple[float, float, dict]]:
        return [(stop["coordinates"][1], stop["coordinates"][0], stop) for stop in required_stops]

    @staticmethod
    def _create_waypoints(route: Route, origin: Location, destination: Location, 
                         intermediate_locations: List[Tuple[float, float, dict]]) -> None:
        waypoints_to_create = []
        order = 0

        waypoints_to_create.append(
            Waypoint(route=route, location=origin, type='pickup', order=order)
        )
        order += 1

        for lat, lon, stop in intermediate_locations:
            stop_location = Location.objects.create(
                name=stop['description'], 
                latitude=lat, 
                longitude=lon
            )
            waypoints_to_create.append(
                Waypoint(route=route, location=stop_location, type=stop['type'], order=order)
            )
            order += 1

        waypoints_to_create.append(
            Waypoint(route=route, location=destination, type='dropoff', order=order)
        )

        Waypoint.objects.bulk_create(waypoints_to_create)

    @staticmethod
    @transaction.atomic
    def create_route_with_stops(
        origin: Location, 
        destination: Location, 
        current_driving_hours: float = 0,
        current_duty_hours: float = 0
    ) -> Route:
        
        origin_dest_waypoints = [(origin.longitude, origin.latitude), (destination.longitude, destination.latitude)]
        total_distance, total_duration, steps, coordinates = RouteOrchestrator._get_api_data(origin_dest_waypoints)
        
        required_stops = RoutingService.calculate_required_stops(
            steps, coordinates, current_driving_hours, current_duty_hours
        )


        intermediate_locations = []
        if required_stops:
            api_waypoints = [origin_dest_waypoints[0]]
            for stop in required_stops:
                api_waypoints.append(tuple(stop["coordinates"]))
            api_waypoints.append(origin_dest_waypoints[1])
            
            total_distance, total_duration, _, _ = RouteOrchestrator._get_api_data(api_waypoints)
            intermediate_locations = RouteOrchestrator._create_intermediate_locations(required_stops)

        service_time = RouteOrchestrator._calculate_service_time(required_stops)
        total_duration += service_time

        route = Route.objects.create(
            origin=origin,
            destination=destination,
            total_distance=total_distance,
            total_duration=total_duration
        )

        RouteOrchestrator._create_waypoints(route, origin, destination, intermediate_locations)
        
        return route