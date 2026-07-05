from rest_framework import serializers
from django.db import transaction
from garage_app.models import Visit
from garage_app.serializers.car import CarReadSerializer, CarWriteSerializer
from garage_app.serializers.service import ServiceOrderReadSerializer, ServiceOrderWriteSerializer
from inventory_app.serializers.product import ProductOrderReadSerializer, ProductOrderWriteSerializer

class VisitWriteSerializer(serializers.ModelSerializer):
    service_orders = ServiceOrderWriteSerializer(many=True, allow_null=True, required=False)
    product_orders = ProductOrderWriteSerializer(many=True, allow_null=True, required=False)
    car = CarWriteSerializer()

    class Meta:
        model = Visit
        fields = '__all__'

    def create(self, validated_data):
        car_data = validated_data.get('car')
        car_obj = CarWriteSerializer().get_or_create_car(car_data)
        validated_data['car'] = car_obj.id
        return super().create(validated_data)

class VisitReadSerializer(serializers.ModelSerializer):
    car = CarReadSerializer(read_only=True)
    service_orders = ServiceOrderReadSerializer(many=True, read_only=True)
    product_orders = ProductOrderReadSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'

class VisitAddServiceOrderSerializer(serializers.Serializer):
    service_orders = ServiceOrderWriteSerializer(many=True)

    def create(self, validated_data):
        visit_id = validated_data.get('visit_id')
        try:
            with transaction.atomic():
                visit = Visit.objects.get(id=visit_id)
                service_orders = validated_data.get('service_orders')
                orders_to_add = []

                for service_order in service_orders:
                    service_order_obj = ServiceOrderWriteSerializer().save_nested(service_order)
                    orders_to_add.append(service_order_obj)

                visit.service_orders.add(*orders_to_add)
        except Visit.DoesNotExist:
            raise serializers.ValidationError("Visit not found")
        return visit
