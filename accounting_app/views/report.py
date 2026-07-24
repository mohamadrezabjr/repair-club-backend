from datetime import date

from django.db.models import Sum, Count, F, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from accounting_app.models import Transaction, Cheque, ChequeStatus, ChequeDirection
from garage_app.models import ServiceOrder
from inventory_app.models import ProductOrder

try:
    # StockEntry ممکن است هنوز مهاجرت نشده باشد؛ ایمپورت امن.
    from inventory_app.models import StockEntry
except Exception:  # pragma: no cover
    StockEntry = None


def _parse_date(value, default):
    if not value:
        return default
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        return default


class AccountingSummaryAPIView(APIView):
    """
    خلاصه‌ی مالی یک بازه (پیش‌فرض: ماه جاری میلادی).
    پارامترها: ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    فرانت بازه‌ی ماه شمسی را به میلادی تبدیل کرده و ارسال می‌کند.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        today = timezone.localdate()
        month_start = today.replace(day=1)
        date_from = _parse_date(request.query_params.get('date_from'), month_start)
        date_to = _parse_date(request.query_params.get('date_to'), today)

        # ── درآمد ──────────────────────────────────────────────
        service_income = ServiceOrder.objects.filter(
            created_at__date__gte=date_from,
            created_at__date__lte=date_to,
        ).aggregate(total=Coalesce(Sum('price'), Value(0)))['total']

        product_income = ProductOrder.objects.filter(
            created_at__date__gte=date_from,
            created_at__date__lte=date_to,
        ).aggregate(
            total=Coalesce(Sum(F('quantity') * F('product__price')), Value(0))
        )['total']

        other_income = Transaction.objects.filter(
            kind='income',
            occurred_at__gte=date_from,
            occurred_at__lte=date_to,
        ).aggregate(total=Coalesce(Sum('amount'), Value(0)))['total']

        income_total = service_income + product_income + other_income

        # ── هزینه‌ها ───────────────────────────────────────────
        purchases = 0
        if StockEntry is not None:
            purchases = StockEntry.objects.filter(
                created_at__date__gte=date_from,
                created_at__date__lte=date_to,
            ).aggregate(
                total=Coalesce(Sum(F('quantity') * F('unit_cost')), Value(0))
            )['total']

        manual_expenses_qs = Transaction.objects.filter(
            kind='expense',
            occurred_at__gte=date_from,
            occurred_at__lte=date_to,
        )
        manual_expenses = manual_expenses_qs.aggregate(
            total=Coalesce(Sum('amount'), Value(0))
        )['total']

        expense_by_category = list(
            manual_expenses_qs.values('category__name')
            .annotate(amount=Coalesce(Sum('amount'), Value(0)))
            .order_by('-amount')
        )
        expense_by_category = [
            {
                'category': row['category__name'] or 'بدون دسته',
                'amount': row['amount'],
            }
            for row in expense_by_category
        ]

        expense_total = purchases + manual_expenses

        # ── چک‌ها ──────────────────────────────────────────────
        def cheque_stats(qs):
            agg = qs.aggregate(
                count=Count('id'),
                amount=Coalesce(Sum('amount'), Value(0)),
            )
            return {'count': agg['count'], 'amount': agg['amount']}

        due_in_range = Cheque.objects.filter(
            status=ChequeStatus.PENDING,
            due_date__gte=date_from,
            due_date__lte=date_to,
        )
        cleared_in_range = Cheque.objects.filter(
            status=ChequeStatus.CLEARED,
            due_date__gte=date_from,
            due_date__lte=date_to,
        )
        overdue = Cheque.objects.filter(
            status=ChequeStatus.PENDING,
            due_date__lt=today,
        )

        return Response({
            'date_from': date_from,
            'date_to': date_to,
            'income': {
                'services': service_income,
                'products': product_income,
                'other': other_income,
                'total': income_total,
            },
            'expense': {
                'purchases': purchases,
                'manual': manual_expenses,
                'by_category': expense_by_category,
                'total': expense_total,
            },
            'profit': income_total - expense_total,
            'cheques': {
                'due': cheque_stats(due_in_range),
                'cleared': cheque_stats(cleared_in_range),
                'overdue': cheque_stats(overdue),
                'received_pending': cheque_stats(
                    Cheque.objects.filter(status=ChequeStatus.PENDING, direction=ChequeDirection.RECEIVED)
                ),
                'issued_pending': cheque_stats(
                    Cheque.objects.filter(status=ChequeStatus.PENDING, direction=ChequeDirection.ISSUED)
                ),
            },
        })
