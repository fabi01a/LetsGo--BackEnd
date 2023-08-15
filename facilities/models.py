from django.db import models
from facilities.user.models import User 
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# User = settings.AUTH_USER_MODEL
    
class Facility(models.Model):
    facility_name = models.CharField(max_length=200)
    facility_address = models.CharField(max_length=200)
    facility_phone = models.CharField(max_length=15)
    facility_directions = models.CharField(max_length=500)
    facility_description = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='favorites')
        
    def __str__(self):
        return self.facility_name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.email

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        post_save.connect(create_profile, sender=User)

def save_profile(sender,instance, **kwargs):
    instance.profile.save()

