from datetime import date

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounting_app.models import Transaction, TransactionCategory
from accounting_app.serializers import (
    TransactionCategorySerializer,
    TransactionReadSerializer,
    TransactionWriteSerializer,
)


def valid_iso_date(value):
    """تاریخ معتبر YYYY-MM-DD را برمی‌گرداند، در غیر این صورت None."""
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


class TransactionCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = TransactionCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = TransactionCategory.objects.all().order_by('name')
        kind = self.request.query_params.get('kind')
        if kind in ('income', 'expense'):
            qs = qs.filter(kind=kind)
        return qs


class TransactionCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class TransactionListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionWriteSerializer
        return TransactionReadSerializer

    def get_queryset(self):
        qs = Transaction.objects.all().select_related('category')
        params = self.request.query_params
        kind = params.get('kind')
        if kind in ('income', 'expense'):
            qs = qs.filter(kind=kind)
        date_from = valid_iso_date(params.get('date_from'))
        date_to = valid_iso_date(params.get('date_to'))
        if date_from:
            qs = qs.filter(occurred_at__gte=date_from)
        if date_to:
            qs = qs.filter(occurred_at__lte=date_to)
        category = params.get('category')
        if category:
            qs = qs.filter(category_id=category)
        return qs


class TransactionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all().select_related('category')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TransactionWriteSerializer
        return TransactionReadSerializer
