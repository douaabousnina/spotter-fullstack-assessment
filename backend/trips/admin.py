from django.contrib import admin
from .models import Location, Route, Waypoint, LogSheet, LogEntry

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'origin', 'destination', 'total_distance', 'total_duration', 'created_at']

@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    list_display = ['route', 'location', 'type', 'order']

@admin.register(LogSheet)
class LogSheetAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'total_driving_hours', 'total_on_duty_hours', 'is_compliant']

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['logsheet', 'status', 'start_time', 'end_time', 'duration']
