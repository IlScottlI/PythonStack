from django.db import models
from dt_planner_app.models import Calendar


class Upload(models.Model):
    upload_file = models.FileField()
    calendar = models.ManyToManyField(
        Calendar,
        related_name='upload_calendar',
        blank=True
    )
    upload_date = models.DateTimeField(auto_now_add=True)
