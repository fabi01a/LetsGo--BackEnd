import os
import requests
from .models import Campsite
from .serializers import CampsiteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


#Function to Handle the user input and use it to make a LocationIQ API call for lat/lon    
def process_campsite_data(ridb_data):
    campsites_data = []
    for facility in ridb_data:
        campsite_data = {
            'facility_name':facility.get('FacilityName'),
            'facility_address': facility.get('FacilityAddress'),
            'facility_phone':facility.get('FacilityPhone'),
            'facility_directions':facility.get('FacilityDirections'),
            'facility_description':facility.get('FacilityDescription'),
            'facility_map_url':facility.get('FacilityMapURL'),
        }
        campsites_data.append(campsite_data)
    return campsites_data


@api_view(['GET'])
def get_campsite_data(request):
    address = request.GET.get('address') #gets the user input for address
    radius = request.GET.get('radius') #gets the user input for distance
    locationiq_api_key = os.environ.get('LOCATIONIQ_API_KEY')
    print("address: ", address)
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
            print('processed_data:', processed_data)

            if not processed_data:
                processed_data = []
            
            response_data = {
                'processed_data': processed_data
            }

            return Response(processed_data, status=ridb_response.status_code)
        
        return Response('Failed to retrieve RIDB API data', status=status.HTTP_200_ok)
    
    return Response('Failed to retrieve LocationIQ API data', status=response.status_code)


#STRETCH GOAL: USER PROFILE?
#function that takes a get request
# @api_view(['GET','POST'])
# def campsites_list(request):

#     if request.method == "GET":
#         campsites = Campsite.objects.all()
#         serializer = CampsiteSerializer(campsites,many=True)
#         return Response(serializer.data)
        

#     if request.method == 'POST':
#         serializer = CampsiteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET','PUT','DELETE'])
# def campsite_detail(request,id):
    
#     try:
#         campsite = Campsite.objects.get(pk=id)
#     except Campsite.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == "GET":
#         serializer = CampsiteSerializer(campsite)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CampsiteSerializer(campsite,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # elif request.method == 'DELETE':
    #     campsite.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


#new view to populate Campsite model with RIDB API data
# @api_view(['GET'])
# def get_campsite_data(request):
#     api_key = os.environ.get('API_KEY')
#     RIDB_URL_API = 'https://ridb.recreation.gov/api/v1/facilities'
#     params = {
#         "latitude": 32.311569,
#         "longitude": -110.929070,
#         "radius": 20,
#         "activity":"CAMPING",
#         "apikey": api_key,
#     }
