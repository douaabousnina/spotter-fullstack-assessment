from django.db import models
from core.models import BaseModel

class Location(BaseModel):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name