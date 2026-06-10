from django.urls import path
from services_app.views.car import CarCreateAPIView, CarListAPIView, CarModelListAPIView, CarModelCreateAPIView, \
    CarUpdateAPIView, CarRetrieveAPIView, CarModelRetrieveAPIView, CarModelUpdateAPIView
from services_app.views.visit import VisitCreateAPIView

urlpatterns = [
    path('cars/create', CarCreateAPIView.as_view(), name="car_create"),
    path('cars/', CarListAPIView.as_view(), name="car_list"),
    path('cars/<int:pk>', CarRetrieveAPIView.as_view(), name="car_retrieve"),
    path('cars/update/<int:pk>', CarUpdateAPIView.as_view(), name="car_update"),
    path('models/', CarModelListAPIView.as_view(), name="car_model_list"),
    path('models/<int:pk>', CarModelRetrieveAPIView.as_view(), name="car_model_retrieve"),
    path('models/<int:pk>/update', CarModelUpdateAPIView.as_view(), name="car_model_update"),
    path('models/create/', CarModelCreateAPIView.as_view(), name="car_model_create"),
    path('visits/create', VisitCreateAPIView.as_view(), name="visit_create"),
]