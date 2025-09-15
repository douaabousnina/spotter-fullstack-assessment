from rest_framework import serializers

from .location import LocationSerializer
from .waypoint import WaypointSerializer
from trips.models import Route

class RouteSerializer(serializers.ModelSerializer):
    origin = LocationSerializer()
    destination = LocationSerializer()
    waypoints = WaypointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'origin', 'destination', 'total_distance', 'total_duration', 'waypoints']
