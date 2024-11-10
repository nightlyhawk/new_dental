from django.db import models
from doctors.models import Doctor, Procedure
from clinics.models import Clinic

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=200) 
    d_o_b = models.DateField() 
    address = models.CharField(max_length=200) 
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    gender_choices = [
        (MALE, "M"),
        (FEMALE, "F"),
        (OTHER, "O"),
    ]
    gender = models.CharField(max_length=6,
                              choices=gender_choices,
                              default=OTHER)
    ssn_last_4 = models.CharField(max_length=4, default="4444")
    phone_number = models.IntegerField()
    def __str__(self):
        return self.name

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name="patient_visits")
    visit_date = models.DateField()
    visit_time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name="patient_visited")
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name="patients_seen")
    procedures = models.ManyToManyField(Procedure, blank=True)
    doctors_notes = models.TextField()

    def __str__(self):
        return self.patient.name
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name="patient_appointment")
    last_visit_date = models.DateField() 
    last_visit_time = models.TimeField()
    last_visit_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name="doctor_last_appointment")
    last_visit_procedures = models.ManyToManyField(Procedure, blank=True, related_name="past_patient_procedures")
    next_appointment = models.BooleanField(default=False)
    next_appointment_date = models.DateField() 
    next_appointment_time = models.TimeField() 
    next_appointment_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name="doctor_next_appointment")
    next_appointment_procedure  = models.ForeignKey(Procedure, on_delete=models.DO_NOTHING, related_name="patient_current_procedure")

    def __str__(self):
        return self.patient.name + ' --- ' + self.last_visit_date.strftime('%Y-%m-%d')