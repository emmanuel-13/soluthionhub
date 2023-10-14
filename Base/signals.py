from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import *
from django.conf import settings


@receiver(post_save, sender=User)
def user_update(sender, created, instance, **kwargs):
    if created:
        send_mail(subject=f"Welcome {instance.username}" ,message="Welcome to Solution Groups we are happy you are here", from_email=settings.EMAIL_HOST, recipient_list=[instance.username])
    
@receiver(post_save, sender=Room)
def send_new_room_notification(sender, created, instance, *args, **kwargs):
    if created:
        for users in User.objects.all():
            send_mail(subject=f"Room Notifications", message="Genk a new room has been created successfully", from_email=settings.EMAIL_HOST, recipient_list=[users])
            
            
            
# @receiver(post_save, sender=User)
# def update_user(sender,created, instance, **kwargs):
#     if User.objects.filter(email=instance.email).exists():
#         send_mail(subject="Profile Update", message=f"Welcome to Solution Groups {instance.username}, your profile has been updated successfully", from_email=settings.EMAIL_HOST, recipient_list=[instance.username])
#     else:
#         pass
