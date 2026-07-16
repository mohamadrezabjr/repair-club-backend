from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Q
from garage_app.models import Visit
from garage_app.serializers.visit import VisitReadSerializer, VisitWriteSerializer, VisitAddOrdersSerializer

class VisitListCreateAPIView(ListCreateAPIView):
    queryset = Visit.objects.all().select_related('car__owner__profile', 'car__model').prefetch_related('service_orders', 'product_orders')
    permission_classes = [IsAdminUser, IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VisitWriteSerializer
        return VisitReadSerializer

class VistRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all().select_related('car__owner__profile', 'car__model').prefetch_related('service_orders', 'product_orders')
    permission_classes = [IsAdminUser, IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VisitWriteSerializer
        return VisitReadSerializer

class VisitAddOrdersAPIView(CreateAPIView):
    serializer_class = VisitAddOrdersSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def perform_create(self, serializer):
        visit_id = self.kwargs.get('visit_id')
        serializer.save(visit_id=visit_id)

class VisitSearchAPIView(ListAPIView):
    serializer_class = VisitReadSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):
        qs = Visit.objects.all().select_related(
            'car__owner__profile', 'car__model'
        ).prefetch_related('service_orders', 'product_orders')

        plate_first = self.request.query_params.get('plate_first', '').strip()
        plate_letter = self.request.query_params.get('plate_letter', '').strip()
        plate_second = self.request.query_params.get('plate_second', '').strip()
        plate_region = self.request.query_params.get('plate_region', '').strip()
        phone = self.request.query_params.get('phone', '').strip()
        date_from = self.request.query_params.get('date_from', '').strip()
        date_to = self.request.query_params.get('date_to', '').strip()

        filters = Q()

        # Search by plate number (individual fields)
        if plate_first:
            filters &= Q(car__plate_first__icontains=plate_first)
        if plate_letter:
            filters &= Q(car__plate_letter__icontains=plate_letter)
        if plate_second:
            filters &= Q(car__plate_second__icontains=plate_second)
        if plate_region:
            filters &= Q(car__plate_region__icontains=plate_region)

        # Search by owner phone number
        if phone:
            filters &= Q(car__owner__phone__icontains=phone)

        # Filter by date range
        if date_from:
            filters &= Q(created_at__date__gte=date_from)
        if date_to:
            filters &= Q(created_at__date__lte=date_to)

        return qs.filter(filters).order_by('-created_at')
