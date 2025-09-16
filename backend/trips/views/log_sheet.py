from rest_framework import generics, status
from rest_framework.response import Response
from datetime import datetime

from trips.models import LogSheet
from trips.serializers import LogSheetSerializer
from trips.orchestrators import ELDOrchestrator

class LogSheetListCreateView(generics.ListCreateAPIView):
    queryset = LogSheet.objects.all().prefetch_related('entries')
    serializer_class = LogSheetSerializer

    def create(self, request, *args, **kwargs):
        """
        Generate ELD log sheet from route data
        Expected input format:
        {
            "route_data": {
                "total_duration": 69419.257,
                "waypoints": [
                    {"type": "pickup", "location": {"latitude": 48.8584, "longitude": 2.2945}, "order": 1},
                    {"type": "rest", "location": {"latitude": 52.292889, "longitude": 12.91091}, "order": 2},
                    {"type": "dropoff", "location": {"latitude": 52.2319, "longitude": 21.0067}, "order": 3}
                ]
            },
            "start_datetime": "2024-06-16T06:00:00" (optional)
        }
        """
        try:
            route_data = request.data.get('route_data')
            if not route_data:
                return Response(
                    {"error": "Route data is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Parse optional start datetime
            start_datetime = None
            start_datetime_str = request.data.get('start_datetime')
            if start_datetime_str:
                start_datetime = datetime.fromisoformat(start_datetime_str.replace('Z', '+00:00'))
            
            # Create log sheet using orchestrator
            # log_sheet = ELDOrchestrator.create_log_sheet_from_route(route_data, start_datetime)
            
            # Serialize and return
            serializer = self.get_serializer(log_sheet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create log sheet: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogSheetRetrieveView(generics.RetrieveAPIView):
    queryset = LogSheet.objects.all().prefetch_related('entries')
    serializer_class = LogSheetSerializer
    lookup_field = 'id'