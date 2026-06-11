from rest_framework import serializers
from services_app.models import Service


class ServiceCreateSerializer(serializers.ModelSerializer):
    """ Serializer for creating new services. """
    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'car_model',
            'base_price',
        ]

class ServiceUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for updating existing services. """
    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'car_model',
            'base_price',
        ]