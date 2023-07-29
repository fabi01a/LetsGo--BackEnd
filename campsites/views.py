import os
import requests
from .models import Campsite
from .serializers import CampsiteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#function that takes a get request
@api_view(['GET','POST'])
def campsites_list(request):

    if request.method == "GET":
        campsites = Campsite.objects.all()
        serializer = CampsiteSerializer(campsites,many=True)
        return Response(serializer.data)
        

    if request.method == 'POST':
        serializer = CampsiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def campsite_detail(request,id):
    
    try:
        campsite = Campsite.objects.get(pk=id)
    except Campsite.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = CampsiteSerializer(campsite)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CampsiteSerializer(campsite,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        campsite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#new view to populate Campsite model with RIDB API data
@api_view(['GET'])
def get_campsite_data(request):
    api_key = os.environ.get('API_KEY')
    RIDB_URL_API = 'https://ridb.recreation.gov/api/v1/facilities'
    params = {
        "latitude": 32.311569,
        "longitude": -110.929070,
        "radius": 20,
        "activity":"CAMPING",
        "apikey": api_key,
    }
    
#API request to RIDB
    response = requests.get(RIDB_URL_API,params=params)

    if response.status_code == 200:
        data = response.json()
        rec_data = data.get('RECDATA',[])

        #Loop through the data, collect into a list
        campsites_data = []
        for facility in rec_data:
            campsite_data = {
                'facility_name':facility.get('FacilityName'),
                'facility_phone':facility.get('FacilityPhone'),
                'facility_directions':facility.get('FacilityDirections'),
                'facility_description':facility.get('FacilityDescription'),
                'facility_map_url':facility.get('FacilityMapURL'),
            }
            campsites_data.append(campsite_data)

        return Response(campsites_data,status=status.HTTP_200_OK)
    else:
        return Response('Failed to retrieve API data', status=response.status_code) 