from facilities.user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer
from .models import Profile

class ProfileAPI(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        print("user:", user)
        profile = get_object_or_404(Profile, user_id=user)#resolve this:how to query, not user=user
        print("profile", profile)
        profile_serializer = ProfileSerializer(profile)
        return Response(profile_serializer.data)