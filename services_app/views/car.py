from rest_framework import generics
from services_app.serializers.car import CarCreateSerializer, CarListSerializer, CarModelSerializer, CarUpdateSerializer
from services_app.models.car import Car, CarModel
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CarCreateAPIView(generics.CreateAPIView):
    serializer_class = CarCreateSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

class CarListAPIView(generics.ListAPIView):
    serializer_class = CarListSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

class CarRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CarListSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

class CarModelListAPIView(generics.ListAPIView):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

class CarModelRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

class CarModelCreateAPIView(generics.CreateAPIView):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

class CarUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CarUpdateSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]