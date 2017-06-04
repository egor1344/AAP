from main.models import Apartment
from rest_framework import serializers


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('id', 'title', 'link', 'price', 'city', 'date_time', 'site')

class ApartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('id', 'title', 'link', 'price', 'price_m2', 'date_time', 'city',
                  'agent', 'site', 'address', 'address', 'floor', 'living_space',
                   'rooms', 'district',  'type_house',  'active')
