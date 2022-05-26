from django.db import models
from django.utils.timezone import now

from vbb.libraries.models import Library


class Announcement(models.Model):
    """
    Announcement model for Libraries
    """

    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    text = models.TextField(default="")
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)
