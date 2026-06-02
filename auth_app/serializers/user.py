from rest_framework import serializers
from auth_app.models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects"""
    class Meta:
        model = User
        fields = [
            'id',
            'phone',
        ]
class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'phone',
            'password',
            'profile',
        ]

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        profile = Profile.objects.create(**profile, user=user)
        return UserSerializer(user).data