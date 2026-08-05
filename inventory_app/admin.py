from django.contrib import admin
from inventory_app.models import Product, ProductType, ProductOrder, StockEntry


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'selling_price', 'purchase_price', 'stock', 'updated_at')
    list_filter = ('product_type',)
    search_fields = ('name',)


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'created_at')


@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'unit_cost', 'supplier', 'created_at')
    search_fields = ('product__name', 'supplier')
    date_hierarchy = 'created_at'
