from django.contrib import admin
from services_app.models.car import Car, CarModel
from services_app.models.service import Service, ServiceOrder
from services_app.models.visit import Visit

admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Service)
admin.site.register(ServiceOrder)
admin.site.register(Visit)