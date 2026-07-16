from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from garage_app.models.staff import Staff, StaffRole
from garage_app.serializers.staff import StaffReadSerializer, StaffWriteSerializer, StaffRoleSerializer


class StaffRoleListCreateAPIView(generics.ListCreateAPIView):
    queryset = StaffRole.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StaffRoleSerializer


class StaffRoleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StaffRole.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StaffRoleSerializer


class StaffListCreateAPIView(generics.ListCreateAPIView):
    queryset = Staff.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StaffWriteSerializer
        return StaffReadSerializer


class StaffRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return StaffWriteSerializer
        return StaffReadSerializer
