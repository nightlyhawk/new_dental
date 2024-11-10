from django.contrib import admin
from .models import Patient, Appointment, Visit

# Register your models here.
admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Appointment)