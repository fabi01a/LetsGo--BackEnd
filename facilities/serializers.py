from rest_framework import serializers
from .models import UserProfile, Facility

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'name', 'date_created']

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id','facility_name','facility_address','facility_phone','facility_directions','facility_description','facility_map_url']