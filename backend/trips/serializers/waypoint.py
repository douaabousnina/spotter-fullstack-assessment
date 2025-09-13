from rest_framework import serializers

from .location import LocationSerializer
from trips.models import Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Waypoint
        fields = ['id', 'location', 'type', 'order']