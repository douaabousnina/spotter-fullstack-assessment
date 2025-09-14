from django.db import models

from core.models import BaseModel

class LogSheet(BaseModel):
    date = models.DateField()
    total_driving_hours = models.FloatField(default=0)
    total_on_duty_hours = models.FloatField(default=0)
    is_compliant = models.BooleanField(default=True)