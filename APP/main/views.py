from django.shortcuts import render
from .models import Apartment
from .serilializers import ApartmentSerializer
from rest_framework import viewsets

class ApartmentsViewSet(viewsets.ModelViewSet):
    """
    API for apartment
    """
    queryset = Apartment.objects.all().order_by('-date_time')
    serializer_class = ApartmentSerializer
