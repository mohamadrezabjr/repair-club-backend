from django.urls import path
from garage_app.views.car import CarListCreateAPIView, CarRetrieveUpdateDestroyAPIView, CarModelListCreateAPIView, \
    CarModelRetrieveUpdateDestroyAPIView, car_is_in_garage
from garage_app.views.service import ServiceRetrieveUpdateDestroyAPIView, ServiceListCreateAPIView, \
    ServiceOrderListCreateAPIView, ServiceOrderRetrieveUpdateDestroyAPIView
from garage_app.views.staff import StaffListCreateAPIView, StaffRetrieveUpdateDestroyAPIView, StaffRoleListCreateAPIView, StaffRoleRetrieveUpdateDestroyAPIView
from garage_app.views.visit import VisitListCreateAPIView, VistRetrieveUpdateDestroyAPIView, VisitAddOrdersAPIView, VisitSearchAPIView

urlpatterns = [
    path('cars/', CarListCreateAPIView.as_view(), name="car_list"),
    path('cars/<int:pk>', CarRetrieveUpdateDestroyAPIView.as_view(), name="car_retrieve"),

    path('models/', CarModelListCreateAPIView.as_view(), name="car_model_list_create"),
    path('models/<int:pk>', CarModelRetrieveUpdateDestroyAPIView.as_view(), name="car_model_retrieve_update_destroy"),

    path('services/', ServiceListCreateAPIView.as_view(), name="service_list_create"),
    path('services/<int:pk>', ServiceRetrieveUpdateDestroyAPIView.as_view(), name="service_retrieve_update_destroy"),

    path('service_orders/', ServiceOrderListCreateAPIView.as_view(), name="service_order_list_create"),
    path('service_orders/<int:pk>/', ServiceOrderRetrieveUpdateDestroyAPIView.as_view(), name="service_order_retrieve_update_destroy"),

    path('staff/', StaffListCreateAPIView.as_view(), name="staff_list_create"),
    path('staff/<int:pk>/', StaffRetrieveUpdateDestroyAPIView.as_view(), name="staff_retrieve_update_destroy"),
    path('staff/roles/', StaffRoleListCreateAPIView.as_view(), name="staff_role_list_create"),
    path('staff/roles/<int:pk>/', StaffRoleRetrieveUpdateDestroyAPIView.as_view(), name="staff_role_retrieve_update_destroy"),

    path('visits/search/', VisitSearchAPIView.as_view(), name="visit_search"),
    path('visits/', VisitListCreateAPIView.as_view(), name="visit_list_create"),
    path('visits/<int:pk>/', VistRetrieveUpdateDestroyAPIView.as_view(), name="visit_retrieve_update_destroy"),
    path('visits/<int:visit_id>/orders/', VisitAddOrdersAPIView.as_view(), name="visit_add_orders"),

    path('cars/is_in_garage/', car_is_in_garage, name="car_is_in_garage"),
]
