from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from garage_app.models import Visit
from garage_app.serializers.visit import VisitReadSerializer, VisitWriteSerializer, VisitAddServiceOrderSerializer

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

class VisitAddServiceOrderAPIView(CreateAPIView):
    serializer_class = VisitAddServiceOrderSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def perform_create(self, serializer):
        visit_id = self.kwargs.get('visit_id')
        serializer.save(visit_id=visit_id)
