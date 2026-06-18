from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from garage_app.models import Service, ServiceOrder
from garage_app.serializers.service import ServiceWriteSerializer, ServiceReadSerializer, ServiceOrderWriteSerializer, ServiceOrderReadSerializer

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all().select_related('car_model')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceWriteSerializer
        return ServiceReadSerializer

class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all().select_related('car_model')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', "PUT"]:
            return ServiceWriteSerializer
        return ServiceReadSerializer

class ServiceOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceOrder.objects.all().select_related('service__car_model')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceOrderWriteSerializer
        return ServiceOrderReadSerializer

class ServiceOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceOrder.objects.all().select_related('service__car_model')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ServiceOrderWriteSerializer
        return ServiceOrderReadSerializer