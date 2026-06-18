from django.urls import path
from services_app.views.car import CarCreateAPIView, CarListAPIView, CarModelListAPIView, CarModelCreateAPIView, \
    CarUpdateAPIView, CarRetrieveAPIView, CarModelRetrieveAPIView, CarModelUpdateAPIView
from services_app.views.service import ServiceRetrieveUpdateDestroyAPIView, ServiceListCreateAPIView, \
    ServiceOrderListCreateAPIView, ServiceOrderRetrieveUpdateDestroyAPIView
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

    path('services/', ServiceListCreateAPIView.as_view(), name="service_list_create"),
    path('services/<int:pk>', ServiceRetrieveUpdateDestroyAPIView.as_view(), name="service_retrieve_update_destroy"),

    path('service_orders/', ServiceOrderListCreateAPIView.as_view(), name="service_order_list_create"),
    path('service_orders/<int:pk>/', ServiceOrderRetrieveUpdateDestroyAPIView.as_view(), name="service_order_retrieve_update_destroy"),

    path('visits/create', VisitCreateAPIView.as_view(), name="visit_create"),

]