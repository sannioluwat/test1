from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.ListRooms.as_view(), name="all"),
    path("new/", views.CreateRoom.as_view(), name="create"),
]
