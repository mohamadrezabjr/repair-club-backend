from django.urls import path
from inventory_app.views.product import ProductListAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, \
    ProductDeleteAPIView, ProductCreateAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),
]