from django.db import models
from services_app.models.car import Car
from services_app.models.service import ServiceOrder

class Visit(models.Model):
    VISIT_STATUS_CHOICES = [
        ('ready', "آماده تحویل"),
        ('queued', "در نوبت"),
        ('repairing', 'درحال تعمیر'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    ]
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(ServiceOrder, blank=True, null=True, related_name='visits')
#   products    TODO
    status = models.CharField(choices=VISIT_STATUS_CHOICES, max_length=30, default='queued')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_ready(self):
        """ Check if all services are done. """
        return not self.services.exclude(status='done').exists()