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
        
    @transaction.atomic
    def create(self, validated_data):
        service_orders_data = validated_data.pop('service_orders', [])
        product_orders_data = validated_data.pop('product_orders', [])
        
        car_data = validated_data.pop('car')
        car_obj = CarWriteSerializer().get_or_create_car(car_data)
        
        if car_obj.is_in_garage():
            raise serializers.ValidationError({'car': 'Car is in garage.'})

        visit = Visit.objects.create(car=car_obj, **validated_data)
        
        service_orders_to_add = []
        product_orders_to_add = []
        
        for service_order_data in service_orders_data:
            service_order = ServiceOrderWriteSerializer().save_nested(service_order_data)
            service_orders_to_add.append(service_order)
            
        for product_order_data in product_orders_data:
            serializer = ProductOrderWriteSerializer(data=product_order_data)   
            serializer.is_valid(raise_exception=True)
            product_order = serializer.save()
            product_orders_to_add.append(product_order)
            
        if service_orders_to_add:
            visit.service_orders.set(service_orders_to_add)
        if product_orders_to_add:
            visit.product_orders.set(product_orders_to_add)

        visit.save()
        
        return visit
        

class VisitReadSerializer(serializers.ModelSerializer):
    car = CarReadSerializer(read_only=True)
    service_orders = ServiceOrderReadSerializer(many=True, read_only=True)
    product_orders = ProductOrderReadSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'

class VisitAddOrdersSerializer(serializers.Serializer):
    service_orders = ServiceOrderWriteSerializer(many=True, required=False)
    product_orders = ProductOrderWriteSerializer(many=True, required=False)

    def create(self, validated_data):
        visit_id = validated_data.get('visit_id')
        try:
            with transaction.atomic():
                visit = Visit.objects.get(id=visit_id)
                service_orders = validated_data.get('service_orders', [])
                service_orders_to_add = []

                for service_order in service_orders:
                    service_order_obj = ServiceOrderWriteSerializer().save_nested(service_order)
                    service_orders_to_add.append(service_order_obj)

                visit.service_orders.add(*service_orders_to_add)

                product_orders = validated_data.get('product_orders', [])
                product_orders_to_add = []
        
                for product_order in product_orders:
                    serializer = ProductOrderWriteSerializer(data=product_order)
                    serializer.is_valid(raise_exception=True)
                    product_order_obj = serializer.save()
                    product_orders_to_add.append(product_order_obj)
        
                visit.product_orders.add(*product_orders_to_add)
        except Visit.DoesNotExist:
            raise serializers.ValidationError("Visit not found")
        return visit
