from django.db import models
from core.models import BaseModel

class Leg(BaseModel):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()