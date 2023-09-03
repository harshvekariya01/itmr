from django.shortcuts import render

from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import *
from mainapp.models import *

# Create your views here.

class ProjectListAPIView(ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    serializer_class = ProjectListSerializer
    queryset = URLDetail.objects.all()


    # data = {}
    # return response(data,status=status.HTTP_200_OK)