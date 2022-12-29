from django.urls import reverse
# from django.contrib.auth.mixins import(
#     LoginRequiredMixin,
#     PermissionRequiredMixin
# )
from django.views import generic
from . import models
from roomtypes.models import RoomType
# Create your views here.


class CreateRoomType(generic.CreateView):
    fields = ("name", "price", "desc", "priority")
    model = RoomType


class ListRoomTypes(generic.ListView):
    model = RoomType
