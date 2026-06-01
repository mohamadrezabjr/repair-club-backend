from django.urls import path
from services_app.views.car import CarCreateAPIView, CarListAPIView
urlpatterns = [
    path('cars/create', CarCreateAPIView.as_view(), name="car_create"),
    path('cars/', CarListAPIView.as_view(), name="car_list"),
]