from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from django.db.models import Sum, Count, F, Value, IntegerField
from django.db.models.functions import Coalesce

from inventory_app.models import Product, StockEntry
from inventory_app.serializers.stock import (
    StockEntryReadSerializer,
    StockEntryWriteSerializer,
)

LOW_STOCK_DEFAULT = 5


class StockEntryListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StockEntryWriteSerializer
        return StockEntryReadSerializer

    def get_queryset(self):
        qs = StockEntry.objects.all().select_related('product')
        product = self.request.query_params.get('product')
        if product:
            qs = qs.filter(product_id=product)
        return qs


class StockEntryRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = StockEntry.objects.all().select_related('product')
    serializer_class = StockEntryReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @transaction.atomic
    def perform_destroy(self, instance):
        product = Product.objects.select_for_update().get(pk=instance.product.pk)
        product.stock = max(0, product.stock - instance.quantity)
        product.save(update_fields=['stock', 'updated_at'])
        instance.delete()


class InventoryReportAPIView(APIView):
    """
    گزارش کلی انبار: تعداد کالاها، مجموع واحدهای موجود، ارزش ریالی موجودی،
    و فهرست کالاهای رو به اتمام. ?threshold=<n>
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            threshold = int(request.query_params.get('threshold', LOW_STOCK_DEFAULT))
        except (TypeError, ValueError):
            threshold = LOW_STOCK_DEFAULT

        products = Product.objects.all()
        agg = products.aggregate(
            product_count=Count('id'),
            total_units=Coalesce(Sum('stock'), Value(0)),
            total_value=Coalesce(
                Sum(F('stock') * F('price'), output_field=IntegerField()),
                Value(0),
            ),
        )

        low_stock = list(
            products.filter(stock__lte=threshold)
            .order_by('stock')
            .values('id', 'name', 'stock', 'price')
        )
        out_of_stock = products.filter(stock__lte=0).count()

        return Response({
            'product_count': agg['product_count'],
            'total_units': agg['total_units'],
            'total_value': agg['total_value'],
            'out_of_stock_count': out_of_stock,
            'low_stock_threshold': threshold,
            'low_stock': low_stock,
        })
