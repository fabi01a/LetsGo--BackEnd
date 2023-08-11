from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    #changes name of entries on admin site
    def __str__(self):
        return self.name
    
    
class Facility(models.Model):
    facility_name = models.CharField(max_length=200)
    facility_address = models.CharField(max_length=200)
    facility_phone = models.CharField(max_length=15)
    facility_directions = models.CharField(max_length=500)
    facility_description = models.CharField(max_length=1000)
        

    def __str__(self):
        return self.facility_name
