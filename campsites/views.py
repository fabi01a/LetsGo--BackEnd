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
