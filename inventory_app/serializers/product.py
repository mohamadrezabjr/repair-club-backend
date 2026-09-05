from rest_framework import serializers
from inventory_app.models import Product, ProductType, ProductOrder
from django.db import transaction

class ProductTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model = ProductType
        fields = '__all__'

    def get_or_create_product_type(self, validated_data):
        id = validated_data.get('id')
        if id:
            try:
                product_type = ProductType.objects.get(id=id)
                return product_type
            except ProductType.DoesNotExist:
                raise serializers.ValidationError(f"product_type with id {id} does not exist.")
        product_type = ProductType.objects.create(**validated_data)
        return product_type
        
class ProductReadSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class ProductWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    product_type = ProductTypeSerializer(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    purchase_price = serializers.BigIntegerField(required=False, allow_null=True)
    selling_price = serializers.BigIntegerField(required=False, allow_null=True)
    stock = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        
    @transaction.atomic
    def get_or_create_product(self, validated_data):
        id = validated_data.get('id')

        if id:
            try:
                product = Product.objects.select_for_update().get(id=id)
                return product
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"product with id {id} does not exist.")

        product_type_data = validated_data.get('product_type')
        product_type_obj = None
        if product_type_data:
            product_type_obj = ProductTypeSerializer().get_or_create_product_type(product_type_data)

        validated_data['product_type'] = product_type_obj
        return Product.objects.create(**validated_data)

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('id', None)
        return self.get_or_create_product(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data.pop('id', None)

        if 'product_type' in validated_data:
            product_type_data = validated_data.pop('product_type')
            if product_type_data:
                instance.product_type = ProductTypeSerializer().get_or_create_product_type(product_type_data)
            else:
                instance.product_type = None

        for attr in ('name', 'selling_price', 'purchase_price', 'stock', 'description'):
            if attr in validated_data and validated_data[attr] is not None:
                setattr(instance, attr, validated_data[attr])

        instance.save()
        return instance

class ProductOrderReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    total_price = serializers.BigIntegerField(read_only=True)
    class Meta:
        model = ProductOrder
        fields = '__all__'

class ProductOrderWriteSerializer(serializers.ModelSerializer):
    product = ProductWriteSerializer()
    
    class Meta:
        model = ProductOrder
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        product_data = validated_data.get('product')
        quantity = validated_data.get('quantity')

        product = ProductWriteSerializer().get_or_create_product(product_data)

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