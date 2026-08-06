from django.db.models import Q
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

class CarSearchAPIView(generics.ListAPIView):
    serializer_class = CarReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = Car.objects.all().select_related('owner__profile', 'model')

        filters = Q()

        plate_first = self.request.query_params.get('plate_first', '').strip()
        plate_letter = self.request.query_params.get('plate_letter', '').strip()
        plate_second = self.request.query_params.get('plate_second', '').strip()
        plate_region = self.request.query_params.get('plate_region', '').strip()
        phone = self.request.query_params.get('phone', '').strip()

        visit_date_from = self.request.query_params.get('visit_date_from', '').strip()
        visit_date_to = self.request.query_params.get('visit_date_to', '').strip()

        if plate_first:
            filters &= Q(plate_first__icontains=plate_first)
        if plate_letter:
            filters &= Q(plate_letter__icontains=plate_letter)
        if plate_second:
            filters &= Q(plate_second__icontains=plate_second)
        if plate_region:
            filters &= Q(plate_region__icontains=plate_region)

        if phone:
            filters &= Q(owner__phone__icontains=phone)

        if visit_date_from:
            filters &= Q(last_visit_date__date__gte=visit_date_from)
        if visit_date_to:
            filters &= Q(last_visit_date__date__lte=visit_date_to)

        return queryset.filter(filters).order_by('-registration_date')









