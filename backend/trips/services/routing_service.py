import requests
from typing import List, Tuple, Dict
from django.conf import settings

from core.constants import MAX_DRIVING_HOURS, MAX_DUTY_WINDOW_HOURS, MAX_FUEL_RANGE_MILES, FUEL_STOP_TIME, PICKUP_DROPOFF_TIME


class RoutingService:
    BASE_URL = settings.GEOAPIFY_BASE_URL

    @staticmethod
    def get_route_from_api(waypoints: List[Tuple[float, float]]) -> Dict:
        waypoints_str = "|".join(f"lonlat:{lon},{lat}" for lon, lat in waypoints)
        params = {
            "waypoints": waypoints_str,
            "mode": "truck",
            "units": "imperial",
            "apiKey": settings.GEOAPIFY_API_KEY
        }
        response = requests.get(RoutingService.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


    @staticmethod
    def calculate_required_stops(
        steps: List[Dict],
        coordinates: List[List[float]],
        current_driving_hours: float = 0,
        current_duty_hours: float = 0,
    ) -> List[Dict]:
        
        stops = []
        
        accumulated_driving_time = current_driving_hours * 60
        accumulated_duty_time = current_duty_hours * 60
        
        accumulated_distance = 0.0

        accumulated_duty_time += PICKUP_DROPOFF_TIME # initial pickup

        for step in steps:
            step_time_minutes = step["time"] / 60.0
            step_distance = step["distance"]

            accumulated_driving_time += step_time_minutes
            accumulated_duty_time += step_time_minutes
            
            accumulated_distance += step_distance

            stop_reason = None
            
            if accumulated_driving_time >= MAX_DRIVING_HOURS * 60:
                stop_reason = "rest"
                accumulated_driving_time = 0.0
                accumulated_duty_time = 0.0
                
            elif accumulated_duty_time >= MAX_DUTY_WINDOW_HOURS * 60:
                stop_reason = "rest"
                accumulated_driving_time = 0.0
                accumulated_duty_time = 0.0
                
            elif accumulated_distance >= MAX_FUEL_RANGE_MILES:
                stop_reason = "fuel"
                accumulated_duty_time += FUEL_STOP_TIME
                accumulated_distance = 0.0

            if stop_reason:
                coord_index = step["to_index"]
                if 0 <= coord_index < len(coordinates[0]):
                    lon, lat = coordinates[0][coord_index]
                    stops.append({
                        "type": stop_reason,
                        "coordinates": [lon, lat]
                    })

        return stops