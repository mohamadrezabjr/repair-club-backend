from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from inventory_app.models import Product, ProductType, ProductOrder
from inventory_app.serializers.product import ProductReadSerializer, ProductWriteSerializer, ProductTypeSerializer, \
    ProductOrderWriteSerializer, ProductOrderReadSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().prefetch_related('product_type')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductWriteSerializer
        return ProductReadSerializer

class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().prefetch_related('product_type')
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get_serializer_class(self):
        if self.request.method in  ['PUT', 'PATCH']:
            return ProductWriteSerializer
        return ProductReadSerializer

class ProductTypeListCreateAPIView(ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProductTypeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProductOrderListCreateAPIView(ListCreateAPIView):
    queryset = ProductOrder.objects.all().select_related('product')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductOrderWriteSerializer
        return ProductOrderReadSerializer

class ProductOrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductOrder.objects.all().select_related('product')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductOrderWriteSerializer
        return ProductOrderReadSerializer