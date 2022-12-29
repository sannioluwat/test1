from django.db import models
from roomtypes.models import RoomType
# Create your models here.
from django.conf import settings
from django.urls import reverse
from datetime import time


class Room(models.Model):
    name = models.CharField(unique=True, max_length=20)
    desc = models.TextField(blank=True, null=True)
    # available_from = models.TimeField(default=time(14))
    # available_till = models.TimeField(default=time(0))
    # pics = ''  # input pictures
    dispprior = models.IntegerField()  # logic for order
    roomtype = models.ForeignKey(
        RoomType, related_name="rooms", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('rooms:all')

    class Meta:
        ordering = ["dispprior"]
