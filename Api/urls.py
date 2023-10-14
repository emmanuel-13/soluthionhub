from django.urls import path
from .views import *

urlpatterns = [
    path('', Rooms),
    path('<int:pk>/', GetRooms),
]
