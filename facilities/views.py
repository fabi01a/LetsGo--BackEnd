import os
import requests
from .models import Facility, Profile
from facilities.user.models import User
from facilities.auth.serializers import RegisterSerializer
from facilities.user.serializers import UserSerializer
from .serializers import FacilitySerializer, ProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView


# HANDLE USER INPUT -> USE FOR LAT/LON LOCATIONIQ API CALL   
def process_campsite_data(ridb_data):
    campsites_data = []
    for facility in ridb_data:

        #get MEDIA image from URL
        # media_list = facility.get('MEDIA', [])
        # image_url = next((media['URL'] for media in media_list if media['URL'].lower().endswith('.jpeg')),None)
        # # if not image_url:
        #     image_url = 'default_image.jpg'

        campsite_data = {
            'facility_name':facility.get('FacilityName'),
            'facility_address': {
                'street_address': None,
                'city': None,
                'state': None,
                'postal_code': None,
            },
            'facility_phone':facility.get('FacilityPhone'),
            'facility_directions':facility.get('FacilityDirections'),
            'facility_description':facility.get('FacilityDescription'),
            # 'facility_image_url': image_url,
        }
        # print("****************CAMPSITE DATA********************")
        # print('campsite_data:',campsite_data)

        facility_address_data = facility.get('FACILITYADDRESS',[])
        
        if facility_address_data:
            facility_address = facility_address_data[0]
            # print("****************FACILITY ADDRESS DATA********************")
            # print('facility address data:', facility_address_data)

            campsite_data['facility_address'] = {
                # 'facility_id': facility_address.get('FacilityID'),
                'street_address':facility_address.get('FacilityStreetAddress1'),
                'city': facility_address.get('City'),
                'state': facility_address.get('AddressStateCode'),
                'postal_code': facility_address.get('PostalCode')
            }
    
        campsites_data.append(campsite_data)

    return campsites_data

#API CALLS
@api_view(['GET'])
def get_campsite_data(request):
    address = request.GET.get('address') #gets the user input for address
    radius = request.GET.get('radius') #gets the user input for distance
    locationiq_api_key = os.environ.get('LOCATIONIQ_API_KEY')
    if not address:
        return Response("An Address or Zipcode is required", status=status.HTTP_400_BAD_REQUEST)
    
    #Make LocationIQ API call to get lat/lon
    locationiq_url = f'https://us1.locationiq.com/v1/search.php?key={locationiq_api_key}&q={address}&format=json'
    response = requests.get(locationiq_url)

    if response.status_code == 200:
        data = response.json()
        latitude = data[0].get('lat')
        longitude = data[0].get('lon')

        #Use the lat/lon/radius to make API call to RIDB
        api_key = os.environ.get('RIDB_API_KEY')
        ridb_url = 'https://ridb.recreation.gov/api/v1/facilities'
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'full': True,
            'radius': radius, #user input
            'activity': 'CAMPING',
            'apikey':api_key,
        }
        #API call to RIDB
        ridb_response = requests.get(ridb_url, params=params)

        if ridb_response.status_code == 200:
            ridb_data = ridb_response.json().get('RECDATA', [])
            #process the RIDB data using created function
            processed_data = process_campsite_data(ridb_data)

            if not processed_data:
                processed_data = []

            response_data = {
                'processed_data': processed_data
            }

            return Response(processed_data, status=ridb_response.status_code)
    
        return Response(processed_data, status=ridb_response.status_code)
        
    return Response('Failed to retrieve RIDB API data', status=status.HTTP_200_ok)


#USER / REGISTRATION
@api_view(['POST'])  
@permission_classes([AllowAny])  # Allow unauthenticated access for registration
def register(request):
    data = request.data
    #check if email/password provided
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user with the same email already exists
    if User.objects.filter(email=email).exists():
        return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.create_user(username=email, email=email, password=password)
    
    # Create user profile (if applicable)
    profile = Profile.objects.create(user=user, bio='this is an example')
    
    # Replace UserProfile with your actual profile model and data

    # Serialize the user profile data
    serialized_user = UserSerializer(user)
    
    # Process registration logic
    return Response({'message': 'Registration successful', 'user': serialized_user.data})


# GET REQUEST : RETRIEVE USER PROFILE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user #gets the authenticated user from request
    profile = user.userprofile #retrieves user profile using the 1-2-many relationshup between user model and userProfile model
    serialized_profile = UserSerializer(user, context={'request': request})
    return Response(serialized_profile.data)#returns serialized profile data as HTTP response


#FAVORITES ROUTES
# CREATE / RETRIEVE USER'S FAVORITES
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorite_facilities(request): 
    user = request.user
    
    if request.method == "GET":  
        favorite_facilities = user.userprofile.favorite_facilities.all() #retrieves user's fav facilities 
        serialized_facilities = serialized_facilities(favorite_facilities)
        return Response(serialized_facilities)#returns serialized facilities as HTTP response

    if request.method == 'POST':
        serializer = FacilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userprofile=user.userprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE / DELETE USER'S FAVORITES 
@api_view(['PUT','DELETE'])
def adjusting_favorite_facilities(request,id):
    try:
        facility = Facility.objects.get(pk=id)
    except Facility.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = FacilitySerializer(facility,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'DELETE':
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class UserProfileAPIView(RetrieveUpdateAPIView):
#     """
#     Get, Update user profile
#     """
#     serializer = ProfileSerializer(favorite_facilities, many=True)

#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_object(self):
#         return self.request.user.profile
