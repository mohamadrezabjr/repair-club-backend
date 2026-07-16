from django.db import models
from garage_app.models.car import Car
from garage_app.models.service import ServiceOrder
from garage_app.models.staff import Staff

class Visit(models.Model):
    VISIT_STATUS_CHOICES = [
        ('ready', "آماده تحویل"),
        ('queued', "در نوبت"),
        ('repairing', 'درحال تعمیر'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    ]
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, related_name='visits')
    service_orders = models.ManyToManyField(ServiceOrder, blank=True, related_name='visits')
    product_orders = models.ManyToManyField("inventory_app.ProductOrder", blank=True, related_name='visits')
    status = models.CharField(choices=VISIT_STATUS_CHOICES, max_length=30, default='queued')
    staff = models.ManyToManyField(Staff, blank=True, related_name='visits', verbose_name="سرویس‌کاران")
    current_mileage = models.PositiveIntegerField(null=True, blank=True, verbose_name="کیلومتر فعلی")
    next_mileage = models.PositiveIntegerField(null=True, blank=True, verbose_name="کیلومتر بعدی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    @property
    def is_ready(self):
        """ Check if all services are done. """
        return not self.service_orders.exclude(status='done').exists()