from rest_framework import serializers
from django.db import transaction
from inventory_app.models import Product, StockEntry
from inventory_app.serializers.product import ProductReadSerializer


class StockEntryReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    total_cost = serializers.IntegerField(read_only=True)

    class Meta:
        model = StockEntry
        fields = '__all__'


class StockEntryWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    # قیمت اختیاری است؛ اگر وارد نشود قیمت فعلی کالا حفظ می‌شود
    unit_selling_price = serializers.BigIntegerField(required=False, allow_null=True)
    unit_purchase_price = serializers.BigIntegerField(required=False, allow_null=True)
    class Meta:
        model = StockEntry
        fields = [
            'id',
            'product',
            'quantity',
            'unit_purchase_price',
            'unit_selling_price',
            'supplier',
            'description'
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("تعداد باید بزرگ‌تر از صفر باشد.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        product = Product.objects.select_for_update().get(pk=validated_data['product'].pk)

        new_selling_price = validated_data.get('unit_selling_price')
        new_purchase_price = validated_data.get('unit_purchase_price')

        update_fields = ['stock', 'updated_at']

        if new_selling_price:
            product.selling_price = new_selling_price
            update_fields.append('selling_price')
        else:
            validated_data['unit_selling_price'] = product.selling_price

        if new_purchase_price:
            product.purchase_price = new_purchase_price
            update_fields.append('purchase_price')
        else:
            validated_data['unit_purchase_price'] = product.purchase_price

        entry = StockEntry.objects.create(**validated_data)
        product.stock += entry.quantity
        product.save(update_fields=update_fields)
        return entry
