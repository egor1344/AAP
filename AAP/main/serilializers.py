from .models import Apartment
from rest_framework import serializers


class ApartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Apartment
        fields = ('title', 'link', 'price', 'city', 'date_time', 'site')