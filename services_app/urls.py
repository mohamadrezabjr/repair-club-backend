from django.urls import path
from services_app.views.car import CarCreateAPIView, CarListAPIView, CarModelListAPIView
from services_app.views.visit import VisitCreateAPIView

urlpatterns = [
    path('cars/create', CarCreateAPIView.as_view(), name="car_create"),
    path('cars/', CarListAPIView.as_view(), name="car_list"),
    path('models/', CarModelListAPIView.as_view(), name="car_model_list"),
    path('visits/create', VisitCreateAPIView.as_view(), name="visit_create"),
]