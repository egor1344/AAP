from main.models import Apartment
from .serilializers import ApartmentSerializer, ApartmentDetailSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics

class ApartmentDetail(APIView):

    def get_apartment(self, id):
        try:
            return Apartment.objects.get(id=id)
        except Apartment.DoesNotExist:
            raise Http404


    def get(self, request, id, format=None):
        apartment = self.get_apartment(id)
        apart_serilize = ApartmentDetailSerializer(apartment)
        return Response(apart_serilize.data)

class ApartmentsViewSet(generics.ListCreateAPIView):
    """
    API for apartment
    """
    queryset = Apartment.objects.all().order_by('-date_time')
    serializer_class = ApartmentSerializer
