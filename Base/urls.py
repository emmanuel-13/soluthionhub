from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_user, name="login_user"),
    path('register/', register_user, name="register_user"),
    path('logout/', logout_user, name="logout_user"),
    path('update_user/', edit_user, name="edit_user"),
    path('topics/', topics, name="topics"),
    path('activity/', ActivityView.as_view(), name="activity"),
    path('rooms/<str:pk>', room, name='rooms'),
    path('profile/<str:pk>', userprofile, name='profile'),
    path('room_form/', room_form, name='room_form'),
    path('room_update/<name>/', room_update, name='room_update'),
    path('room_delete/<name>/', room_delete, name='room_delete'),
    path('room_message/<str:pk>/', room_message_delete, name='message'),
]
