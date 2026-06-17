from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from inventory_app.models import Product
from inventory_app.serializers.product import ProductReadSerializer, ProductWriteSerializer

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all().prefetch_related('product_type')
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all().prefetch_related('product_type')
    serializer_class = ProductReadSerializer

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all().prefetch_related('product_type')
    serializer_class = ProductReadSerializer

class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all().prefetch_related('product_type')
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all().prefetch_related('product_type')
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

