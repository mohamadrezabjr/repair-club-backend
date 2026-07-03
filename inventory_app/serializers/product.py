from rest_framework import serializers
from inventory_app.models import Product, ProductType, ProductOrder
from django.db import transaction

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductReadSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductOrderReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    total_price = serializers.BigIntegerField(read_only=True)
    class Meta:
        model = ProductOrder
        fields = '__all__'

class ProductOrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        product_obj = validated_data.get('product')
        quantity = validated_data.get('quantity')

        product = Product.objects.select_for_update().get(pk=product_obj.pk)

        if product.stock < quantity:
            raise serializers.ValidationError({'quantity': 'Not enough stock'})

        product.stock -= quantity
        product.save()

        validated_data['product'] = product

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        product = Product.objects.select_for_update().get(pk=instance.product.pk)

        new_quantity = validated_data.get('quantity', instance.quantity)
        difference = new_quantity - instance.quantity

        if difference > product.stock:
            raise serializers.ValidationError({'quantity': 'Not enough stock'})

        product.stock -= difference
        product.save()

        return super().update(instance, validated_data)