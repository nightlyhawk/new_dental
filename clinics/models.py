from django.db import models
from doctors.models import Doctor

# Create your models here.
class Clinic(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    doctors = models.ManyToManyField(Doctor, blank=True, related_name="working_in")


    def __str__(self):
        return self.name