from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.


class RoomType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()
    desc = models.TextField()
    priority = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)

    def get_absolute_url(self):
        return reverse('roomtypes:all')
