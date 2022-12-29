from django.urls import path
from . import views

app_name = 'roomtypes'


urlpatterns = [
    path('', views.ListRoomTypes.as_view(), name="all"),
    path("new/", views.CreateRoomType.as_view(), name="create"),
]
