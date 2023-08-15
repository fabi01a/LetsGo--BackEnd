from facilities.user.models import User
from facilities.user.serializers import UserSerializer
from facilities.auth.serializers import RegisterSerializer
from rest_framework import filters, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated']
    ordering = ['-updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        lookup_kwargs = {self.lookup_field: lookup_field_value}
        obj = get_object_or_404(User, **lookup_kwargs)

        # obj = User.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj

class UserRegistrationView(generics.CreateAPIView):
    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self,request, *args, **kwargs):
        print('RECEIVED REGISTRATION REQ:', request.data)
        serializer = self.get_serializer(data=request.data)
        print('SERIALIZER DATA:', serializer.initial_data)

        if serializer.is_valid():
            print("Serializer is valid")
        else:
            print("Serializer errors:", serializer.errors)  # Add this line to print serializer errors

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print("Error during registration:", str(e))  # Add this line to print any exceptions

            return Response(
                {'error': 'An error occurred during registration'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
