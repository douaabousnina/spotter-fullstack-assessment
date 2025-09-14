from django.db import models

from .route import Route
from .location import Location

from core.models import BaseModel
from core.constants import WAYPOINT_TYPE_CHOICES

class Waypoint(BaseModel):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='waypoints')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=WAYPOINT_TYPE_CHOICES)
    order = models.PositiveIntegerField()
