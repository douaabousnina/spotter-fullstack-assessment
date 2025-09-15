import requests
from typing import List, Tuple, Dict
from django.conf import settings
from datetime import datetime, timedelta

from core.constants import (
    MAX_DRIVING_HOURS,
    MAX_DUTY_WINDOW_HOURS,
    MAX_DRIVING_TIME_CYCLE,
    MAX_FUEL_RANGE_MILES,
    FUEL_STOP_TIME,
    PICKUP_DROPOFF_TIME,
    REQUIRED_BREAK_HOURS,
)


class RoutingService:
    BASE_URL = settings.GEOAPIFY_BASE_URL

    @staticmethod
    def get_route_from_api(waypoints: List[Tuple[float, float]]) -> Dict:
        waypoints_str = "|".join(f"lonlat:{lon},{lat}" for lon, lat in waypoints)
        params = {
            "waypoints": waypoints_str,
            "mode": "truck",
            "units": "imperial",
            "apiKey": settings.GEOAPIFY_API_KEY,
        }
        response = requests.get(RoutingService.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data

    @staticmethod
    def calculate_required_stops(
        legs: List[Dict],
        steps_time: List[List[float]],
        steps_distance: List[List[float]],
        steps_from_index: List[List[int]],
        coordinates: List[List[float]],
        current_cycle_hours: float = 0.0,
    ) -> List[Dict]:
        
        stops = []
        current_time = datetime.now()
        
        daily_driving_seconds = 0.0
        daily_duty_seconds = 0.0  
        weekly_duty_seconds = current_cycle_hours*3600
        
        current_distance = 0.0
        
        order_counter = 1

        stops.append({
            "type": "current",
            "coordinates": coordinates[0][0],
            "timestamp": current_time.isoformat() + "Z",
            "daily_driving": daily_driving_seconds/3600,
            "daily_duty": daily_duty_seconds/3600,
            "weekly_driving": current_cycle_hours,
            "distance_traveled": current_distance,
            "order": order_counter
        })
        order_counter += 1
        
        if current_cycle_hours >= MAX_DRIVING_TIME_CYCLE:
            stops.append(
                {
                    "type": "current",
                    "coordinates": coordinates[0][0],
                    "timestamp": current_time.isoformat() + "Z",
                    "daily_driving": daily_driving_seconds/3600,
                    "daily_duty": daily_duty_seconds/3600,
                    "weekly_driving": current_cycle_hours,
                    "distance_traveled": current_distance,
                    "order": order_counter
                }
            )
            
            

        for leg_index, leg in enumerate(legs):
            leg_seconds = leg["duration"]
            leg_distance = leg["distance"]
            leg_coordinates = coordinates[leg_index]

            if (
                daily_driving_seconds + leg_seconds <= MAX_DRIVING_HOURS * 3600
                and daily_duty_seconds + leg_seconds <= MAX_DUTY_WINDOW_HOURS * 3600
                and current_distance + leg_distance <= MAX_FUEL_RANGE_MILES
            ):
                current_distance += leg_distance
                daily_driving_seconds += leg_seconds
                daily_duty_seconds += leg_seconds
                weekly_duty_seconds += leg_seconds
                current_time += timedelta(seconds=leg["duration"])
                
                
                
            else:
                leg_steps_distance = steps_distance[leg_index]
                leg_steps_time = steps_time[leg_index]
                leg_steps_from_index = steps_from_index[leg_index]
                
                for idx in range(len(leg_steps_distance)):
                    stop_added = False
                    step_coords = leg_coordinates[leg_steps_from_index[idx]]

                    step_time = leg_steps_time[idx]
                    step_distance = leg_steps_distance[idx]

                    if current_distance + step_distance >= MAX_FUEL_RANGE_MILES:
                        stop_time = current_time + timedelta(seconds=step_time)

                        stops.append({
                            "type": "fuel",
                            "coordinates": step_coords,
                            "timestamp": stop_time.isoformat() + "Z",
                            "daily_driving": daily_driving_seconds/3600,
                            "daily_duty": daily_duty_seconds/3600,
                            "weekly_driving": current_cycle_hours + daily_driving_seconds/3600,
                            "distance_traveled": current_distance + step_distance,
                            "order": order_counter
                        })
                        order_counter += 1

                        current_distance = 0.0
                        current_time = stop_time + timedelta(hours=FUEL_STOP_TIME)
                        daily_duty_seconds += FUEL_STOP_TIME * 3600
                        weekly_duty_seconds += FUEL_STOP_TIME * 3600
                        stop_added = True

                    if daily_driving_seconds + step_time >= MAX_DRIVING_HOURS * 3600:
                        stop_time = current_time + timedelta(seconds=step_time)

                        stops.append({
                            "type": "rest",
                            "coordinates": step_coords,
                            "timestamp": stop_time.isoformat() + "Z",
                            "daily_driving": daily_driving_seconds/3600,
                            "daily_duty": daily_duty_seconds/3600,
                            "weekly_driving": current_cycle_hours + daily_driving_seconds/3600,
                            "distance_traveled": current_distance + step_distance,
                            "order": order_counter
                        })
                        order_counter += 1

                        current_time = stop_time + timedelta(hours=REQUIRED_BREAK_HOURS)
                        daily_driving_seconds = 0.0
                        daily_duty_seconds = 0.0 # ! important?
                        stop_added = True
                        
                    if daily_duty_seconds + step_time >= MAX_DUTY_WINDOW_HOURS * 3600:
                        stop_time = current_time + timedelta(seconds=step_time)

                        stops.append({
                            "type": "rest",
                            "coordinates": step_coords,
                            "timestamp": stop_time.isoformat() + "Z",
                            "daily_driving": daily_driving_seconds/3600,
                            "daily_duty": daily_duty_seconds/3600,
                            "weekly_driving": current_cycle_hours + daily_driving_seconds/3600,
                            "distance_traveled": current_distance + step_distance,
                            "order": order_counter
                        })
                        order_counter += 1

                        current_time = stop_time + timedelta(hours=REQUIRED_BREAK_HOURS)
                        daily_driving_seconds = 0.0
                        daily_duty_seconds = 0.0
                        stop_added = True

                    if not stop_added:
                        current_distance += step_distance
                        current_time += timedelta(seconds=step_time)
                        daily_duty_seconds += step_time
                        daily_driving_seconds += step_time
                        weekly_duty_seconds += step_time
                    


            stop_type = "pickup" if leg_index == 0 else "dropoff"
            stop_coords = leg_coordinates[-1]
            stops.append({
                "type": stop_type,
                "coordinates": stop_coords,
                "timestamp": current_time.isoformat() + "Z",
                "daily_driving": daily_driving_seconds/3600,
                "daily_duty": daily_duty_seconds/3600,
                "weekly_driving": current_cycle_hours + daily_driving_seconds/3600,
                "distance_traveled": current_distance,
                "order": order_counter
            })
            order_counter += 1

            current_time += timedelta(hours=PICKUP_DROPOFF_TIME)
            daily_duty_seconds += PICKUP_DROPOFF_TIME*3600

        return stops