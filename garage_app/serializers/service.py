from rest_framework import serializers
from garage_app.models import Service, ServiceOrder
from garage_app.serializers.car import CarModelReadSerializer
from inventory_app.serializers.product import ProductTypeSerializer


class ServiceWriteSerializer(serializers.ModelSerializer):
    """ Serializer for creating and updating services. """
    class Meta:
        model = Service
        fields = '__all__'

class ServiceReadSerializer(serializers.ModelSerializer):
    """ Serializer for retrieving service information. """
    car_model = CarModelReadSerializer(read_only=True)
    products_needed = ProductTypeSerializer(read_only=True, many=True)
    class Meta:
        model = Service
        fields = '__all__'

class ServiceOrderReadSerializer(serializers.ModelSerializer):
    service = ServiceReadSerializer(read_only=True)
    class Meta:
        model = ServiceOrder
        fields = '__all__'

class ServiceOrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = '__all__'