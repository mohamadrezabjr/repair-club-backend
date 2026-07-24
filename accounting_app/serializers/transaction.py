from rest_framework import serializers
from accounting_app.models import Transaction, TransactionCategory


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = '__all__'


class TransactionReadSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer(read_only=True)
    kind_display = serializers.CharField(source='get_kind_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=TransactionCategory.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Transaction
        fields = [
            'id', 'kind', 'title', 'amount', 'category',
            'payment_method', 'description', 'occurred_at', 'visit',
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("مبلغ باید بزرگ‌تر از صفر باشد.")
        return value

    def validate(self, attrs):
        category = attrs.get('category')
        kind = attrs.get('kind', getattr(self.instance, 'kind', None))
        if category and kind and category.kind != kind:
            raise serializers.ValidationError(
                {'category': 'نوع دسته با نوع تراکنش هم‌خوانی ندارد.'}
            )
        return attrs
