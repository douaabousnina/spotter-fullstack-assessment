from django.db import models

from .location import Location

from core.models import BaseModel 

class Route(BaseModel):
    origin = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='routes_origin')
    destination = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='routes_destination')
    total_distance = models.FloatField()
    total_duration = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    