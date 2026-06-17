from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth_app.views.user import user_register, UserTempCreateAPIView, auth_me

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('register/', user_register, name="register"),
    path('temp-register/', UserTempCreateAPIView.as_view(), name="temp-register"),
    path('auth_me/', auth_me, name="auth_me"),
]