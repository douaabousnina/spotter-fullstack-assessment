from rest_framework import generics

from trips.models import Route
from trips.serializers import RouteSerializer

class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def create(self, request, *args, **kwargs):
        route = generate_rout(request.data)
         
        return super().create(request, *args, **kwargs)

class RouteRetrieveView(generics.RetrieveAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    lookup_field = 'id'
