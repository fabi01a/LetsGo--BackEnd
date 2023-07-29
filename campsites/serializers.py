from rest_framework import serializers
from .models import Campsite

class CampsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campsite
        fields = ['id','facility_name','facility_phone','facility_directions','facility_description','facility_map_url']