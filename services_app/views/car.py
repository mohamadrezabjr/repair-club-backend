from rest_framework import generics
from services_app.serializers.car import CarCreateSerializer
from services_app.models.car import Car
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CarCreateView(generics.CreateAPIView):
    serializer_class = CarCreateSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]