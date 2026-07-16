from django.db import transaction
from rest_framework import serializers
from garage_app.models import Service, ServiceOrder, Staff
from garage_app.serializers.car import CarModelReadSerializer
from garage_app.serializers.staff import StaffReadSerializer
from inventory_app.serializers.product import ProductTypeSerializer


class ServiceWriteSerializer(serializers.ModelSerializer):
    """ Serializer for creating and updating services. """
    id = serializers.IntegerField(allow_null=True, required=False)
    title = serializers.CharField(max_length=100, required=False, allow_null=True)
    products_needed = ProductTypeSerializer(many=True, required=False, allow_null=True)

    @transaction.atomic
    def get_or_create_service(self, validated_data):

        service_id = validated_data.get('id')
        if service_id:
            try:
                return Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                raise serializers.ValidationError("Service does not exist")
                
        products_needed_data = validated_data.pop('products_needed')
        products_needed_to_add = []

        for product_data in products_needed_data:
            products_needed_to_add.append(ProductTypeSerializer().get_or_create_product_type(product_data))
            
        service = Service.objects.create(**validated_data)
        if products_needed_to_add:
            service.products_needed.set(products_needed_to_add)
        service.save()
        return service

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
    staff = StaffReadSerializer(many=True, read_only=True)
    class Meta:
        model = ServiceOrder
        fields = '__all__'

class ServiceOrderWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    service = ServiceWriteSerializer()
    staff = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), many=True, required=False, allow_null=True)


    @transaction.atomic
    def save_nested(self, validated_data):

        service_order_id = validated_data.get('id')
        staff_data = validated_data.pop('staff', [])
        if service_order_id:
            try:
                service_order = ServiceOrder.objects.get(id=service_order_id)
            except ServiceOrder.DoesNotExist:
                raise serializers.ValidationError("Service order does not exist")
        else:
            service_data = validated_data.pop('service')
            service = ServiceWriteSerializer().get_or_create_service(service_data)
            service_order = ServiceOrder.objects.create(service=service, **validated_data)

        if staff_data:
            service_order.staff.set(staff_data)
        return service_order

    class Meta:
        model = ServiceOrder
        fields = '__all__'
