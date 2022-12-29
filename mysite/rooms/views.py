# from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from rooms.models import Room
from . import models

# Create your views here.


class CreateRoom (LoginRequiredMixin, generic.CreateView):
    fields = ("name", "desc", "dispprior", "roomtype")
    model = Room


class ListRooms(generic.ListView):
    model = Room
    # select_related = ("roomtype")...didn't make a difference
