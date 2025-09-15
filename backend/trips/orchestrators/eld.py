from datetime import datetime
from typing import Dict, List

from trips.models import LogSheet, LogEntry
from trips.services import ELDService

class ELDOrchestrator:
    
    @staticmethod
    def create_log_sheet_from_route(route_data: Dict, start_datetime: datetime = None) -> LogSheet:
        """
        Create ELD log sheet from route data with waypoints
        """
        # Generate ELD events from route
        events = ELDService.generate_eld_events_from_route(route_data, start_datetime)
        
        if not events:
            raise ValueError("No events generated from route data")
        
        # Process events into time range entries
        processed_entries = ELDService.process_events_to_entries(events)
        
        # Calculate daily totals
        daily_totals = ELDService.calculate_daily_totals(processed_entries)
        
        # Check compliance
        is_compliant = ELDService.check_compliance(
            daily_totals['total_driving_hours'],
            daily_totals['total_on_duty_hours']
        )
        
        # Get date from first event
        log_date = datetime.strptime(events[0]['date'], "%Y-%m-%d").date()
        
        # Create LogSheet
        log_sheet = LogSheet.objects.create(
            date=log_date,
            total_driving_hours=daily_totals['total_driving_hours'],
            total_on_duty_hours=daily_totals['total_on_duty_hours'],
            is_compliant=is_compliant
        )
        
        # Create LogEntry instances
        for entry_data in processed_entries:
            LogEntry.objects.create(
                logsheet=log_sheet,
                status=entry_data['status'],
                start_time=entry_data['start_time'],
                end_time=entry_data['end_time'],
                duration=entry_data['duration']
            )
        
        return log_sheet