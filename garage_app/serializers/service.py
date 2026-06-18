from rest_framework import serializers
from garage_app.models import Service, ServiceOrder
from garage_app.serializers.car import CarModelReadSerializer

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
    car_model = CarModelReadSerializer(read_only=True)
    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'car_model',
            'base_price',
        ]

class ServiceOrderReadSerializer(serializers.ModelSerializer):
    service = ServiceReadSerializer(read_only=True)
    class Meta:
        model = ServiceOrder
        fields = '__all__'

class ServiceOrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = '__all__'