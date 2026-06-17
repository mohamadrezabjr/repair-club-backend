from django.urls import path
from inventory_app.views.product import ProductListAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, \
    ProductDeleteAPIView, ProductCreateAPIView, ProductTypeRetrieveAPIView, ProductTypeCreateAPIView, \
    ProductTypeDeleteAPIView, ProductTypeUpdateAPIView, ProductTypeListAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),

    path('product_types/', ProductTypeListAPIView.as_view(), name='product-type-list'),
    path('product_types/<int:pk>/', ProductTypeRetrieveAPIView.as_view(), name='product-type-detail'),
    path('product_types/create/', ProductTypeCreateAPIView.as_view(), name='product-type-create'),
    path('product_types/<int:pk>/update/', ProductTypeUpdateAPIView.as_view(), name='product-type-update'),
    path('product_types/<int:pk>/delete/', ProductTypeDeleteAPIView.as_view(), name='product-type-delete'),
]