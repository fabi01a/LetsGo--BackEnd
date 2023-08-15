from facilities.user.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'created', 'updated', 'favorites']
        read_only_field = ['is_active', 'created', 'updated']