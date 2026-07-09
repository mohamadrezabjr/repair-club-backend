from django.urls import path
from garage_app.views.car import CarListCreateAPIView, CarRetrieveUpdateDestroyAPIView, CarModelListCreateAPIView, CarModelRetrieveUpdateDestroyAPIView
from garage_app.views.service import ServiceRetrieveUpdateDestroyAPIView, ServiceListCreateAPIView, \
    ServiceOrderListCreateAPIView, ServiceOrderRetrieveUpdateDestroyAPIView
from garage_app.views.visit import VisitListCreateAPIView, VistRetrieveUpdateDestroyAPIView, VisitAddOrdersAPIView

urlpatterns = [
    path('cars/', CarListCreateAPIView.as_view(), name="car_list"),
    path('cars/<int:pk>', CarRetrieveUpdateDestroyAPIView.as_view(), name="car_retrieve"),

    path('models/', CarModelListCreateAPIView.as_view(), name="car_model_list_create"),
    path('models/<int:pk>', CarModelRetrieveUpdateDestroyAPIView.as_view(), name="car_model_retrieve_update_destroy"),

    path('services/', ServiceListCreateAPIView.as_view(), name="service_list_create"),
    path('services/<int:pk>', ServiceRetrieveUpdateDestroyAPIView.as_view(), name="service_retrieve_update_destroy"),

    path('service_orders/', ServiceOrderListCreateAPIView.as_view(), name="service_order_list_create"),
    path('service_orders/<int:pk>/', ServiceOrderRetrieveUpdateDestroyAPIView.as_view(), name="service_order_retrieve_update_destroy"),

    path('visits/', VisitListCreateAPIView.as_view(), name="visit_list_create"),
    path('visits/<int:pk>/', VistRetrieveUpdateDestroyAPIView.as_view(), name="visit_retrieve_update_destroy"),
    path('visits/<int:visit_id>/orders/', VisitAddOrdersAPIView.as_view(), name="visit_add_orders"),
]
