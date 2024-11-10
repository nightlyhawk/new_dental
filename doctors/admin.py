from django.contrib import admin
from .models import Procedure, Doctor, Schedule

# Register your models here.
admin.site.register(Procedure)
admin.site.register(Schedule)
admin.site.register(Doctor)
