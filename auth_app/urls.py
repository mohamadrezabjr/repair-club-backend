from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth_app.views.user import user_register

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('register/', user_register, name="register"),
]