from django.db import models
from auth_app.models import User

class CarModel(models.Model):
    class TransmissionTypeChoices(models.TextChoices):
        AUTO = ('auto', 'اتومات')
        MANUAL = ('man', 'دستی')

    make = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(max_length=50)
    model_year = models.IntegerField(null=True, blank=True)
    transmission_type = models.CharField(choices=TransmissionTypeChoices.choices, max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.model}'

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True)
    plate_number = models.CharField(max_length=10,)
    manufacturing_date = models.IntegerField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    in_garage = models.BooleanField(default=True)
    last_visit_date = models.DateTimeField(null=True, blank=True)
    last_mileage = models.IntegerField(null=True, blank=True)