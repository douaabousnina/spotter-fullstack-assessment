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
    REQUIRED_BREAK_HOURS
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
            "apiKey": settings.GEOAPIFY_API_KEY
        }
        response = requests.get(RoutingService.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def calculate_required_stops(
        steps: List[List[Dict]],
        coordinates: List[List[float]],
        current_driving_seconds: float = 0.0,
        current_duty_seconds: float = 0.0,
        current_weekly_driving_seconds: float = 0.0,
    ) -> List[Dict]:

        waypoint_types = ["current", "pickup", "rest", "fuel", "dropoff"]
        current_time = datetime.now()

        accumulated_daily_driving = current_driving_seconds
        accumulated_daily_duty = current_duty_seconds
        accumulated_weekly_driving = current_weekly_driving_seconds
        accumulated_distance = 0.0

        driving_events = []
        if current_driving_seconds > 0:
            start_prior = current_time - timedelta(seconds=current_driving_seconds)
            driving_events.append((start_prior, current_time, current_driving_seconds))

        stops = []

        print(f"\n🚛 STARTING HOS COMPLIANCE CHECK")
        print(f"⏰ Start time: {current_time}")
        print(f"📊 Initial state:")
        print(f"   - Daily driving: {accumulated_daily_driving:.2f}h/{MAX_DRIVING_HOURS}h")
        print(f"   - Daily duty: {accumulated_daily_duty:.2f}h/{MAX_DUTY_WINDOW_HOURS}h")
        print(f"   - Weekly driving: {accumulated_weekly_driving:.2f}h/{MAX_DRIVING_TIME_CYCLE}h")
        print(f"   - Distance traveled: {accumulated_distance:.1f}/{MAX_FUEL_RANGE_MILES} miles")

        # === PROCESS LEGS ===
        for leg_idx, step_list in enumerate(steps):
            target_type = waypoint_types[leg_idx + 1] if leg_idx + 1 < len(waypoint_types) else "driving"
            is_driving_leg = target_type not in ["rest", "fuel"]

            print(f"\n🛣️  === Processing leg {leg_idx} to {target_type} ===")
            print(f"🚗 Is driving leg: {is_driving_leg}")
            print(f"📍 Steps in this leg: {len(step_list)}")

            step_idx = 0
            while step_idx < len(step_list):
                step = step_list[step_idx]
                step_distance_miles = step.get("distance", 0)
                step_time_seconds = step.get("time", 0)

                if step_time_seconds <= 0:
                    step_idx += 1
                    continue

                stop_reason, stop_description = None, ""
                if is_driving_leg and accumulated_daily_driving >= MAX_DRIVING_HOURS * 3600:
                    stop_reason = "rest"
                    stop_description = f"Exceeded daily driving limit ({accumulated_daily_driving:.1f}h)"
                elif is_driving_leg and accumulated_weekly_driving >= MAX_DRIVING_TIME_CYCLE * 3600:
                    stop_reason = "rest"
                    stop_description = f"Exceeded weekly driving cycle ({accumulated_weekly_driving:.1f}h)"
                elif accumulated_distance >= MAX_FUEL_RANGE_MILES:
                    stop_reason = "fuel"
                    stop_description = f"Exceeded fuel range ({accumulated_distance:.1f} mi)"
                elif accumulated_daily_duty >= MAX_DUTY_WINDOW_HOURS * 3600:
                    stop_reason = "rest"
                    stop_description = f"Exceeded daily duty limit ({accumulated_daily_duty:.1f}h)"

                if stop_reason:
                    print(f"🚨 VIOLATION before step {step_idx + 1}: {stop_description}")

                    # Pick stop coordinates (prefer from_index point)
                    stop_coordinates = coordinates[leg_idx][step['from_index']]

                    stops.append({
                        "type": stop_reason,
                        "description": stop_description,
                        "coordinates": stop_coordinates,
                        "timestamp": current_time.isoformat() + "Z",
                        "daily_driving": round(accumulated_daily_driving / 3600, 2),
                        "daily_duty": round(accumulated_daily_duty / 3600, 2),
                        "weekly_driving": round(accumulated_weekly_driving / 3600, 2),
                        "distance_traveled": round(accumulated_distance, 2),
                    })

                    print(f"🛑 ADDED {stop_reason.upper()} STOP at {current_time}")

                    # Handle stop effects
                    if stop_reason == "rest":
                        rest_end_time = current_time + timedelta(hours=REQUIRED_BREAK_HOURS)
                        accumulated_daily_driving = 0.0
                        accumulated_daily_duty = 0.0
                        cutoff_8days = rest_end_time - timedelta(days=8)
                        driving_events = [(s, e, d) for s, e, d in driving_events if e >= cutoff_8days]
                        accumulated_weekly_driving = sum(d for _, _, d in driving_events)
                        current_time = rest_end_time
                        print(f"😴 Rested {REQUIRED_BREAK_HOURS}h → resume at {current_time}")
                    elif stop_reason == "fuel":
                        fuel_end_time = current_time + timedelta(hours=FUEL_STOP_TIME)
                        accumulated_daily_duty += FUEL_STOP_TIME * 3600
                        accumulated_distance = 0.0
                        current_time = fuel_end_time
                        print(f"⛽ Fueled {FUEL_STOP_TIME}h → resume at {current_time}")

                    # ⚠️ Do not consume this step, retry after break
                    continue

                # ✅ Safe to apply this step
                next_time = current_time + timedelta(seconds=step_time_seconds)
                if is_driving_leg:
                    accumulated_daily_driving = step_time_seconds
                    accumulated_weekly_driving = step_time_seconds
                    driving_events.append((current_time, next_time, step_time_seconds))
                if target_type != "rest":
                    accumulated_daily_duty += step_time_seconds
                accumulated_distance += step_distance_miles

                print(f"\n➡️ Step {step_idx + 1}/{len(step_list)}")
                print(f"   ⏰ Time: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   📏 +{step_distance_miles:.2f} mi, +{step_time_seconds:.2f}h")
                print(f"   🚛 Daily driving: {accumulated_daily_driving:.2f}/{MAX_DRIVING_HOURS}h")
                print(f"   📋 Daily duty: {accumulated_daily_duty:.2f}/{MAX_DUTY_WINDOW_HOURS}h")
                print(f"   📅 Weekly driving: {accumulated_weekly_driving:.2f}/{MAX_DRIVING_TIME_CYCLE}h")
                print(f"   ⛽ Distance: {accumulated_distance:.1f}/{MAX_FUEL_RANGE_MILES} mi")

                current_time = next_time
                step_idx += 1

        # === SUMMARY ===
        print(f"\n🏁 === FINAL HOS COMPLIANCE SUMMARY ===")
        print(f"🛑 Total stops generated: {len(stops)}")
        print(f"⏰ Final time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Final state:")
        print(f"   🚛 Daily driving: {accumulated_daily_driving:.2f}/{MAX_DRIVING_HOURS}h")
        print(f"   📋 Daily duty: {accumulated_daily_duty:.2f}/{MAX_DUTY_WINDOW_HOURS}h")
        print(f"   📅 Weekly driving: {accumulated_weekly_driving:.2f}/{MAX_DRIVING_TIME_CYCLE}h")
        print(f"   ⛽ Distance: {accumulated_distance:.1f}/{MAX_FUEL_RANGE_MILES} mi")

        return stops
