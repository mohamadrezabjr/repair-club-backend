from django.contrib import admin
from garage_app.models.car import Car, CarModel
from garage_app.models.service import Service, ServiceOrder
from garage_app.models.visit import Visit

admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Service)
admin.site.register(ServiceOrder)
admin.site.register(Visit)