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
    unit_cost = serializers.BigIntegerField(required=False, allow_null=True)

    class Meta:
        model = StockEntry
        fields = ['id', 'product', 'quantity', 'unit_cost', 'supplier', 'description']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("تعداد باید بزرگ‌تر از صفر باشد.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        product = Product.objects.select_for_update().get(pk=validated_data['product'].pk)

        new_price = validated_data.get('unit_cost')
        update_fields = ['stock', 'updated_at']

        if new_price:
            # قیمت جدید وارد شده → قیمت کالا به‌روزرسانی می‌شود (بالاتر یا پایین‌تر)
            product.price = new_price
            update_fields.append('price')
        else:
            # قیمت وارد نشده → قیمت قبلی حفظ و در تاریخچه‌ی این ورود ثبت می‌شود
            validated_data['unit_cost'] = product.price

        entry = StockEntry.objects.create(**validated_data)
        product.stock += entry.quantity
        product.save(update_fields=update_fields)
        return entry
