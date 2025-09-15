from rest_framework import serializers

from .log_entry import LogEntrySerializer
from trips.models import LogSheet

class LogSheetSerializer(serializers.ModelSerializer):
    entries = LogEntrySerializer(many=True, read_only=True)

    class Meta:
        model = LogSheet
        fields = ['id', 'date', 'total_driving_hours', 'total_on_duty_hours', 'is_compliant', 'entries']
