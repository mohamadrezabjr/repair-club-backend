from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from services_app.models import Service
from services_app.serializers.service import ServiceCreateSerializer, ServiceUpdateSerializer


class ServiceCreateAPIView(generics.CreateAPIView):
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ServiceCreateSerializer

class ServiceUpdateAPIView(generics.UpdateAPIView):
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ServiceUpdateSerializer