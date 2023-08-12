from django.contrib import admin
from facilities.user.models import User
from .models import Facility



admin.site.register(User) 
admin.site.register(Facility) 