from rest_framework import serializers
from trips.models import LogEntry

class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ['id', 'status', 'start_time', 'end_time', 'duration']