from django.db import transaction
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
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = [
            'id',
            'phone',
            'profile',
            'role'
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

class UserTempCreateSerializer(serializers.ModelSerializer):
    """Serializer for user creation with temp password"""
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'phone',
            'profile'
        ]
    @transaction.atomic
    def create(self, validated_data):
        profile = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data, password=validated_data.get('phone'))
        if profile:
            profile = Profile.objects.create(**profile, user=user)
        return user