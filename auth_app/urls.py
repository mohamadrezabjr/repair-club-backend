from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from auth_app.views.user import user_register, UserTempCreateAPIView, auth_me, SearchUserAPIView
from auth_app.views.token import SafeTokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', SafeTokenRefreshView.as_view(), name="refresh"),
    path('register/', user_register, name="register"),
    path('temp-register/', UserTempCreateAPIView.as_view(), name="temp-register"),
    path('auth_me/', auth_me, name="auth_me"),
    path('users/search-by-phone/<str:phone>/', SearchUserAPIView.as_view(), name="search"),
]