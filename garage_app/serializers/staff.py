from rest_framework import serializers
from garage_app.models.staff import Staff, StaffRole


class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = '__all__'


class StaffReadSerializer(serializers.ModelSerializer):
    role = StaffRoleSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'


class StaffWriteSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=StaffRole.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Staff
        fields = '__all__'
