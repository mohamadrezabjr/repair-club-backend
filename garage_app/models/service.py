from django.db import models
from garage_app.models.car import CarModel

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    base_price = models.BigIntegerField(null=True, blank=True)
    products_needed = models.ManyToManyField("inventory_app.ProductType", blank=True, related_name='services')
    mileage_interval = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class ServiceOrder(models.Model):
    SERVICE_STATUS_CHOICES = [
        ('pending', 'درانتظار'),
        ('in-progress', 'در حال انجام'),
        ('done', 'انجام شد')
    ]
    title = models.CharField(max_length=100, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    extra_description = models.TextField(null=True, blank=True)
    price = models.BigIntegerField()
    status = models.CharField(choices=SERVICE_STATUS_CHOICES, max_length=30, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title