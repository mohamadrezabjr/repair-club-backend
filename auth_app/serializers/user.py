from rest_framework import serializers

from auth_app.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects"""
    class Meta:
        model = User
        fields = [
            'id',
            'phone',
        ]