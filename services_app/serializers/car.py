from rest_framework import serializers
from services_app.models.car import Car
from auth_app.models import User

class CarCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='phone', queryset=User.objects.all())
    class Meta:
        model = Car
        fields = [
            'plate_number',
            'owner',
            'model',
            'manufacturing_date',
            'in_garage',
            'last_mileage'
        ]