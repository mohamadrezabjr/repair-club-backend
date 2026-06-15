from rest_framework import serializers
from services_app.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """ Serializer for services. """
    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'car_model',
            'base_price',
        ]