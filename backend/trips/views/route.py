from rest_framework import generics, status
from rest_framework.response import Response

from trips.models import Route, Location
from trips.serializers import RouteSerializer
from trips.orchestrators import RouteOrchestrator

class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def create(self, request, *args, **kwargs):
        try:
            current = request.data.get("current")
            origin = request.data.get("origin")
            destination = request.data.get("destination")
            current_cycle_hours = request.data.get("current_cycle_hours")

            if not origin or not destination or not current:
                return Response(
                    {"error": "origin and destination are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            current_lat = float(current.get("latitude"))
            current_lng = float(current.get("longitude"))
            origin_lat = float(origin.get("latitude"))
            origin_lng = float(origin.get("longitude"))
            dest_lat = float(destination.get("latitude"))
            dest_lng = float(destination.get("longitude"))

            current_location = Location.objects.create(
                name=f"{current_lat},{current_lng}",
                latitude=current_lat,
                longitude=current_lng,
            )
            
            origin_location = Location.objects.create(
                name=f"{origin_lat},{origin_lng}",
                latitude=origin_lat,
                longitude=origin_lng,
            )
            
            destination_location = Location.objects.create(
                name=f"{dest_lat},{dest_lng}",
                latitude=dest_lat,
                longitude=dest_lng,
            )
            

            route = RouteOrchestrator.create_route_with_stops(
                current_location=current_location,
                origin=origin_location,
                destination=destination_location,
                current_cycle_hours=float(current_cycle_hours)
            )
            
            serializer = self.get_serializer(route)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RouteRetrieveView(generics.RetrieveAPIView):
    queryset = Route.objects.select_related('origin', 'destination').prefetch_related('waypoints__location')
    serializer_class = RouteSerializer
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        response_data = serializer.data
        
        return Response(response_data)