from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from services_app.models import Visit
from services_app.serializers.visit import VisitCreateSerializer

class VisitCreateAPIView(CreateAPIView):
    serializer_class = VisitCreateSerializer
    queryset = Visit.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]