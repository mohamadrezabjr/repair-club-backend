from rest_framework import serializers
from accounting_app.models import Cheque


class ChequeSerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Cheque
        fields = '__all__'

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("مبلغ باید بزرگ‌تر از صفر باشد.")
        return value
