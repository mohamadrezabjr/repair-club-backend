from rest_framework import serializers
from services_app.models.car import Car
from auth_app.models import User
from auth_app.serializers.user import UserSerializer

class CarCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='phone', queryset=User.objects.all(), required=False)
    class Meta:
        model = Car
        fields = [
            'owner',
            'model',
            'manufacturing_date',
            'in_garage',
            'last_mileage',
            'plate_first',
            'plate_letter',
            'plate_second',
            'plate_region',
        ]

class CarListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'owner',
            'model',
            'manufacturing_date',
            'in_garage',
            'last_mileage',
            'plate_first',
            'plate_letter',
            'plate_second',
            'plate_region',
            'plate_number',
        ]

    def get_owner(self, obj):
        return UserSerializer(obj.owner).data