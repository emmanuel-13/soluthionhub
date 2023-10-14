from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to="images", default="avatar.svg")
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)
    
    # avater
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    name = models.CharField(max_length=200)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Topics"
        verbose_name = "Topic"
        ordering = ("-updated", "-created")
    
    
    
class Room(models.Model):
    host =  models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name } for {self.topic.name}' 
    
    class Meta:
        verbose_name_plural = "Rooms"
        verbose_name = "Room"
        ordering = ("-updated", )
    
    
 
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    body = models.TextField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.body[0:50]}'
    
    class Meta:
        verbose_name_plural = "Messages"
        verbose_name = "Message"
        ordering = ("-updated", )
    
    

    