from django.urls import path
from inventory_app.views.product import ProductListCreateAPIView, ProductTypeListCreateAPIView,\
    ProductRetrieveUpdateDestroyAPIView, ProductTypeRetrieveUpdateDestroyAPIView, \
    ProductTypeRetrieveUpdateDestroyAPIView,ProductOrderListCreateAPIView, ProductOrderRetrieveUpdateDestroyAPIView
from inventory_app.views.stock import StockEntryListCreateAPIView, StockEntryRetrieveDestroyAPIView, \
    InventoryReportAPIView

urlpatterns = [
    path('report/', InventoryReportAPIView.as_view(), name='inventory-report'),

    path('stock_entries/', StockEntryListCreateAPIView.as_view(), name='stock-entry-list'),
    path('stock_entries/<int:pk>/', StockEntryRetrieveDestroyAPIView.as_view(), name='stock-entry-detail'),

    path('products/', ProductListCreateAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),

    path('product_types/', ProductTypeListCreateAPIView.as_view(), name='product-type-list'),
    path('product_types/<int:pk>/', ProductTypeRetrieveUpdateDestroyAPIView.as_view(), name='product-type-detail'),

    path('product_orders/', ProductOrderListCreateAPIView.as_view(), name='product-order-list'),
    path('product_orders/<int:pk>/', ProductOrderRetrieveUpdateDestroyAPIView.as_view(), name='product-order-detail'),
]