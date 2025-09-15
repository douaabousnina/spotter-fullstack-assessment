from datetime import datetime, timedelta
from typing import List, Dict

from core.constants import (
    MAX_DRIVING_HOURS, MAX_DUTY_WINDOW_HOURS, REQUIRED_BREAK_HOURS,
    PICKUP_DROPOFF_TIME, FUEL_STOP_TIME, MAX_DRIVING_TIME_CYCLE
)

class ELDService:
    
    @staticmethod
    def generate_eld_events_from_route(route_data: Dict) -> List[Dict]:
                
        events = []
        current_time = datetime.now().replace(second=0, microsecond=0)
        
        waypoints = sorted(route_data.get('waypoints', []), key=lambda x: x['order'])
        
        for i, waypoint in enumerate(waypoints):
            wp_type = waypoint['type']
            
            if wp_type == 'current':
                events.append({
                    'time': current_time.strftime('%H:%M'),
                    'date': current_time.strftime('%Y-%m-%d'),
                    'duty_status': 'on_duty',
                    'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                    'description': 'Pre-trip inspection'
                })
                
                if i + 1 < len(waypoints):
                    events.append({
                        'time': current_time.strftime('%H:%M'),
                        'date': current_time.strftime('%Y-%m-%d'),
                        'duty_status': 'driving',
                        'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                        'description': 'Driving to pickup location'
                    })
                    
                    driving_time = ELDService._calculate_segment_time(waypoint, waypoints[i + 1], route_data)
                    current_time += timedelta(minutes=driving_time)
                
            elif wp_type == 'pickup':
                events.append({
                    'time': current_time.strftime('%H:%M'),
                    'date': current_time.strftime('%Y-%m-%d'),
                    'duty_status': 'on_duty',
                    'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                    'description': 'Pickup and loading'
                })
                current_time += timedelta(minutes=PICKUP_DROPOFF_TIME)
                
                if i + 1 < len(waypoints):
                    events.append({
                        'time': current_time.strftime('%H:%M'),
                        'date': current_time.strftime('%Y-%m-%d'),
                        'duty_status': 'driving',
                        'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                        'description': 'Driving to next destination'
                    })
                    
                    driving_time = ELDService._calculate_segment_time(waypoint, waypoints[i + 1], route_data)
                    current_time += timedelta(minutes=driving_time)
            
            elif wp_type == 'rest':
                events.append({
                    'time': current_time.strftime('%H:%M'),
                    'date': current_time.strftime('%Y-%m-%d'),
                    'duty_status': 'off_duty',
                    'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                    'description': 'Mandatory rest break'
                })
                current_time += timedelta(hours=REQUIRED_BREAK_HOURS)
                
                if i + 1 < len(waypoints):
                    events.append({
                        'time': current_time.strftime('%H:%M'),
                        'date': current_time.strftime('%Y-%m-%d'),
                        'duty_status': 'driving',
                        'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                        'description': 'Resume driving after rest'
                    })
                    
                    driving_time = ELDService._calculate_segment_time(waypoint, waypoints[i + 1], route_data)
                    current_time += timedelta(minutes=driving_time)
            
            elif wp_type == 'fuel':
                events.append({
                    'time': current_time.strftime('%H:%M'),
                    'date': current_time.strftime('%Y-%m-%d'),
                    'duty_status': 'on_duty',
                    'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                    'description': 'Fuel stop'
                })
                current_time += timedelta(minutes=FUEL_STOP_TIME)
                
                if i + 1 < len(waypoints):
                    events.append({
                        'time': current_time.strftime('%H:%M'),
                        'date': current_time.strftime('%Y-%m-%d'),
                        'duty_status': 'driving',
                        'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                        'description': 'Resume driving after fuel'
                    })
                    
                    driving_time = ELDService._calculate_segment_time(waypoint, waypoints[i + 1], route_data)
                    current_time += timedelta(minutes=driving_time)
            
            elif wp_type == 'dropoff':
                events.append({
                    'time': current_time.strftime('%H:%M'),
                    'date': current_time.strftime('%Y-%m-%d'),
                    'duty_status': 'on_duty',
                    'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                    'description': 'Delivery and unloading'
                })
                current_time += timedelta(minutes=PICKUP_DROPOFF_TIME)
                
                events.append({
                    'time': current_time.strftime('%H:%M'),
                    'date': current_time.strftime('%Y-%m-%d'),
                    'duty_status': 'off_duty',
                    'location': f"{waypoint['location']['latitude']},{waypoint['location']['longitude']}",
                    'description': 'End of duty'
                })
        
        return events
    
    @staticmethod
    def _calculate_segment_time(from_waypoint: Dict, to_waypoint: Dict, route_data: Dict) -> float:
        total_duration_minutes = route_data.get('total_duration', 0) / 60
        total_waypoints = len(route_data.get('waypoints', []))
        
        # Simple approximation: divide total time by number of segments
        if total_waypoints > 1:
            return total_duration_minutes / (total_waypoints - 1)
        
        return total_duration_minutes
    
    @staticmethod
    def process_events_to_entries(events: List[Dict]) -> List[Dict]:
        """
        Convert individual time events into time ranges with durations
        """
        if not events:
            return []
        
        # Sort events by date and time
        events.sort(key=lambda x: (x['date'], x['time']))
        
        processed_entries = []
        
        for i, event in enumerate(events[:-1]):  # All except last
            next_event = events[i + 1]
            
            # Parse current and next timestamps
            current_datetime = ELDService._parse_datetime(event['date'], event['time'])
            next_datetime = ELDService._parse_datetime(next_event['date'], next_event['time'])
            
            # Calculate duration
            duration = (next_datetime - current_datetime).total_seconds() / 3600  # hours
            
            processed_entries.append({
                'status': event['duty_status'],
                'start_time': current_datetime,
                'end_time': next_datetime,
                'duration': duration,
                'location': event.get('location', ''),
                'description': event.get('description', '')
            })
        
        return processed_entries
    
    @staticmethod
    def _parse_datetime(date_str: str, time_str: str) -> datetime:
        """Parse date and time strings into datetime object"""
        datetime_str = f"{date_str} {time_str}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    
    @staticmethod
    def calculate_daily_totals(entries: List[Dict]) -> Dict:
        """Calculate total driving and on-duty hours"""
        driving_hours = 0
        on_duty_hours = 0
        
        for entry in entries:
            if entry['status'] == 'driving':
                driving_hours += entry['duration']
                on_duty_hours += entry['duration']  # Driving counts as on-duty
            elif entry['status'] == 'on_duty':
                on_duty_hours += entry['duration']
        
        return {
            'total_driving_hours': driving_hours,
            'total_on_duty_hours': on_duty_hours
        }
    
    @staticmethod
    def check_compliance(total_driving_hours: float, total_on_duty_hours: float) -> bool:
        """Check if daily hours comply with HOS regulations"""
        return (total_driving_hours <= MAX_DRIVING_HOURS and 
                total_on_duty_hours <= MAX_DUTY_WINDOW_HOURS)
