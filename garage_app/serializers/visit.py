from rest_framework import serializers
from garage_app.models import Visit
from garage_app.serializers.car import CarReadSerializer
from garage_app.serializers.service import ServiceOrderReadSerializer
from inventory_app.serializers.product import ProductOrderReadSerializer

class VisitWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

class VisitReadSerializer(serializers.ModelSerializer):
    car = CarReadSerializer(read_only=True)
    service_orders = ServiceOrderReadSerializer(many=True, read_only=True)
    product_orders = ProductOrderReadSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'