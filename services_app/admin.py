from django.contrib import admin
from services_app.models.car import Car, CarModel

admin.site.register(CarModel)
admin.site.register(Car)