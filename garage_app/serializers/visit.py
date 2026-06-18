from rest_framework import serializers
from garage_app.models import Visit


class VisitCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = [
            'id',
            'car',
            'services',
            'status'
        ]