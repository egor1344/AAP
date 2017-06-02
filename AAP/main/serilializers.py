from .models import Apartment
from rest_framework import serializers


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('id', 'title', 'link', 'price', 'city', 'date_time', 'site')
