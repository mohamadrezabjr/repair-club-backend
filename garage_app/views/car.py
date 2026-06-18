from rest_framework import generics
from garage_app.serializers.car import CarWriteSerializer, CarReadSerializer, CarModelReadSerializer, CarModelWriteSerializer
from garage_app.models.car import Car, CarModel
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all().select_related("owner__profile", "model")
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarWriteSerializer
        return CarReadSerializer


class CarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all().select_related("owner__profile", "model")
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CarWriteSerializer
        return CarReadSerializer

class CarModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarModelWriteSerializer
        return CarModelReadSerializer


class CarModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CarModelWriteSerializer
        return CarModelReadSerializer