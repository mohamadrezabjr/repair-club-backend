from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from auth_app.models import User
from auth_app.serializers.user import UserRegisterSerializer, UserTempCreateSerializer, UserSerializer


@extend_schema(
    request=UserRegisterSerializer,
)
@api_view(['POST'])
def user_register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserTempCreateAPIView(generics.CreateAPIView):
    serializer_class = UserTempCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

@api_view(['GET'])
def auth_me(request):
    if request.user.is_authenticated:
        data = UserSerializer(request.user).data
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)