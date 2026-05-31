from django.urls import path
from services_app.views.car import CarCreateView
urlpatterns = [
    path('car/create', CarCreateView.as_view(), name="car_create")
]