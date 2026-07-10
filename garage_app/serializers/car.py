import re

from django.db import transaction
from rest_framework import serializers
from garage_app.models.car import Car, CarModel
from auth_app.models import User
from auth_app.serializers.user import UserSerializer, UserTempCreateSerializer

class CarModelReadSerializer(serializers.ModelSerializer):
    """Serializer for CarModel"""
    class Meta:
        model = CarModel
        fields = '__all__'

class CarModelWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    model = serializers.CharField(required=False, allow_blank=True, max_length=100)
    class Meta:
        model = CarModel
        fields = '__all__'

    def get_or_create_model(self, validated_data):
        model_id = validated_data.get('id')
        if model_id:
            try:
                car_model = CarModel.objects.get(pk=model_id)
                return car_model
            except CarModel.DoesNotExist:
                raise serializers.ValidationError(f'CarModel with id {model_id} does not exist')
        car_model = CarModel.objects.create(**validated_data)
        return car_model 

class CarWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    owner = UserTempCreateSerializer(required=False, allow_null=True)
    model = CarModelWriteSerializer(required=False)

    plate_first = serializers.IntegerField(required=False, allow_null=True)
    plate_letter = serializers.CharField(required=False, allow_null=True, max_length = 10)
    plate_second = serializers.IntegerField(required=False, allow_null=True)
    plate_region = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Car
        fields = [
            'id',
            'owner',
            'model',
            'manufacturing_year',
            'last_mileage',
            'plate_first',
            'plate_letter',
            'plate_second',
            'plate_region',
        ]
        validators = []
        
    @transaction.atomic
    def create(self, validated_data):
        model_data = validated_data.pop('model')
        model_obj = CarModelWriteSerializer().get_or_create_model(model_data)
        validated_data['model'] = model_obj

        owner_data = validated_data.pop('owner')
        owner_id = owner_data.pop('id', None)
        if owner_id:
            try:
                owner = User.objects.get(id=owner_id)
                validated_data['owner'] = owner
            except User.DoesNotExist:
                raise serializers.ValidationError(f'Owner with id {owner_id} does not exist')
        else:
            serializer = UserTempCreateSerializer(data=owner_data)
            print("owner_data:", owner_data)
            serializer.is_valid()
            validated_data['owner'] = serializer.save()
        
        plate_first = validated_data.pop('plate_first')
        plate_letter = validated_data.pop('plate_letter')
        plate_second = validated_data.pop('plate_second')
        plate_region = validated_data.pop('plate_region')
        car, created = Car.objects.get_or_create(
            plate_first=plate_first,
            plate_letter=plate_letter,
            plate_second=plate_second,
            plate_region=plate_region,
            defaults=validated_data
        )
        return car
        
    def get_or_create_car(self, validated_data):
        car_id = validated_data.get('id', None)
        if car_id:
            try:
                car = Car.objects.get(id=car_id)
                return car
            except Car.DoesNotExist:
                raise serializers.ValidationError(f"Car with id {car_id} does not exist")
        return self.create(validated_data)
class CarReadSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)
    model = CarModelReadSerializer(read_only=True, required=False)

    class Meta:
        model = Car
        fields = [
            'id',
            'owner',
            'model',
            'manufacturing_year',
            'last_mileage',
            'plate_first',
            'plate_letter',
            'plate_second',
            'plate_region',
            'plate_number',
        ]

class CarIsInGarageSerializer(serializers.Serializer):
    in_garage = serializers.SerializerMethodField(read_only=True)
    plate_first = serializers.IntegerField()
    plate_letter = serializers.CharField(max_length=10)
    plate_second = serializers.IntegerField()
    plate_region = serializers.IntegerField()
    active_visit = serializers.SerializerMethodField(read_only=True)

    def get_in_garage(self, validated_data):
        plate_first = validated_data.get('plate_first')
        plate_letter = validated_data.get('plate_letter')
        plate_second = validated_data.get('plate_second')
        plate_region = validated_data.get('plate_region')

        try:
            car = Car.objects.get(
                plate_first=plate_first,
                plate_letter=plate_letter,
                plate_second=plate_second,
                plate_region=plate_region
            )
            return car.is_in_garage()
        except Car.DoesNotExist:
            return False
    
    def get_active_visit(self, validated_data):
        from garage_app.serializers.visit import VisitReadSerializer
        plate_first = validated_data.get('plate_first')
        plate_letter = validated_data.get('plate_letter')
        plate_second = validated_data.get('plate_second')
        plate_region = validated_data.get('plate_region')

        try:
            car = Car.objects.get(
                plate_first=plate_first,
                plate_letter=plate_letter,
                plate_second=plate_second,
                plate_region=plate_region
            )
            active_visit = car.visits.exclude(status__in=['delivered', 'cancelled']).last()
            if active_visit:
                return VisitReadSerializer(active_visit).data
            return None
        except Car.DoesNotExist:
            return None
