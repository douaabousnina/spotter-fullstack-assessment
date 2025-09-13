from django.db import models

from .log_sheet import LogSheet

from core.models import BaseModel
from core.constants import DUTY_STATUS_CHOICES

class LogEntry(BaseModel):
    logsheet = models.ForeignKey(LogSheet, on_delete=models.CASCADE, related_name='entries')
    status = models.CharField(max_length=20, choices=DUTY_STATUS_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField()  # hours
