from rest_framework import generics
from garage_app.serializers.car import CarWriteSerializer, CarReadSerializer, CarModelReadSerializer, CarModelWriteSerializer, CarIsInGarageSerializer
from garage_app.models.car import Car, CarModel
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

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
        
@extend_schema(
        request=CarIsInGarageSerializer,
        )
@api_view(['POST'])
def car_is_in_garage(request):
    serializer = CarIsInGarageSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
