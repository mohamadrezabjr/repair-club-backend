from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounting_app.models import Cheque
from accounting_app.serializers import ChequeSerializer
from accounting_app.views.transaction import valid_iso_date


class ChequeListCreateAPIView(ListCreateAPIView):
    serializer_class = ChequeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = Cheque.objects.all()
        params = self.request.query_params
        direction = params.get('direction')
        if direction in ('received', 'issued'):
            qs = qs.filter(direction=direction)
        status = params.get('status')
        if status:
            qs = qs.filter(status=status)
        # فیلتر بر اساس بازه‌ی تاریخ سررسید (برای «چک‌های این ماه»)
        due_from = valid_iso_date(params.get('due_from'))
        due_to = valid_iso_date(params.get('due_to'))
        if due_from:
            qs = qs.filter(due_date__gte=due_from)
        if due_to:
            qs = qs.filter(due_date__lte=due_to)
        return qs


class ChequeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
