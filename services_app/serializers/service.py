from rest_framework import serializers
from services_app.models import Service
from services_app.serializers.car import CarModelSerializer

class ServiceWriteSerializer(serializers.ModelSerializer):
    """ Serializer for creating and updating services. """
    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'car_model',
            'base_price',
        ]

class ServiceReadSerializer(serializers.ModelSerializer):
    """ Serializer for retrieving service information. """
    car_model = CarModelSerializer(read_only=True)
    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'car_model',
            'base_price',
        ]