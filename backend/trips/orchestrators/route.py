from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from typing import List, Tuple

from trips.models import Route, Location, Waypoint
from trips.services import RoutingService
from core.constants import PICKUP_DROPOFF_TIME, FUEL_STOP_TIME, REQUIRED_BREAK_HOURS


class RouteOrchestrator:

    @staticmethod
    def _get_api_data(waypoints: List[Tuple[float, float]]) -> tuple:
        api_response = RoutingService.get_route_from_api(waypoints=waypoints)

        if "features" not in api_response or not api_response["features"]:
            raise ValueError(f"Routing API failed: {api_response}")

        feature = api_response['features'][0]
        properties = feature['properties']
        legs_raw = properties['legs']

        legs = []
        for leg in legs_raw:
            legs.append({
                "duration": leg["time"],
                "distance": leg["distance"]
            })

        steps_time = [[step["time"] for step in leg["steps"]] for leg in legs_raw]
        steps_distance = [[step["distance"] for step in leg["steps"]] for leg in legs_raw]
        steps_from_index = [[step.get("from_index") for step in leg["steps"]] for leg in legs_raw]

        return (
            properties['distance'],          # total distance
            properties['time'],              # total duration
            legs,
            steps_time,
            steps_distance,
            steps_from_index,
            feature["geometry"]["coordinates"]  # coordinates
        )

    @staticmethod
    @transaction.atomic
    def create_route_with_stops(
        current_location: Location,
        origin: Location,
        destination: Location,
        current_cycle_hours: float,
        start_time: timezone.datetime = None
    ) -> Route:
        if start_time is None:
            start_time = timezone.now()

        initial_waypoints = [
            (current_location.longitude, current_location.latitude),
            (origin.longitude, origin.latitude),
            (destination.longitude, destination.latitude)
        ]

        total_distance, total_duration, legs, steps_time, steps_distance, steps_from_index, coordinates = RouteOrchestrator._get_api_data(initial_waypoints)

        # Calculate required stops
        required_stops = RoutingService.calculate_required_stops(
            legs=legs,
            steps_time=steps_time,
            steps_distance=steps_distance,
            steps_from_index=steps_from_index,
            coordinates=coordinates,
            current_cycle_hours=current_cycle_hours
        )

        # Create route
        route = Route.objects.create(
            origin=origin,
            destination=destination,
            total_distance=total_distance,
            total_duration=total_duration
        )

        # Create waypoints from stops
        waypoints_to_create = []
        for order, stop in enumerate(required_stops):
            # Determine Location object
            coords = stop["coordinates"]
            if stop["type"] == "current":
                location_obj = current_location
            elif stop["type"] == "pickup":
                location_obj = origin
            elif stop["type"] == "dropoff":
                location_obj = destination
            else:
                # Intermediate stop: create a Location
                location_obj = Location.objects.create(
                    latitude=coords[1],
                    longitude=coords[0],
                    name=stop.get("description", stop["type"].capitalize())
                )

            # Calculate spent time
            if stop["type"] in ["pickup", "dropoff"]:
                spent_time = PICKUP_DROPOFF_TIME
            elif stop["type"] == "fuel":
                spent_time = FUEL_STOP_TIME
            elif stop["type"] == "rest":
                spent_time = REQUIRED_BREAK_HOURS
            else:
                spent_time = 0

            waypoints_to_create.append(
                Waypoint(
                    route=route,
                    location=location_obj,
                    type=stop["type"],
                    order=order,
                    arrival_time=stop["timestamp"],
                    spent_time=spent_time
                )
            )

        Waypoint.objects.bulk_create(waypoints_to_create)
        return route
