from rest_framework import serializers
from inventory_app.models import Product, ProductType


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
