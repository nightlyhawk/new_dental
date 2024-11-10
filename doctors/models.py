from django.db import models

# Create your models here.
class Procedure(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    npi = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.EmailField(default="brightsmile@gmail.com")
    phone_number = models.CharField(max_length=14, default='+234')
    office_address = models.CharField(max_length=200)
    specialties = models.ManyToManyField(Procedure, blank=True)

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="schedule")
    day = models.CharField(max_length=9)
    startTime = models.TimeField()
    endTime = models.TimeField()

    def __str__(self):
        return self.doctor.name
