from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.BigIntegerField()
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, related_name='products')
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)