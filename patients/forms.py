from django import forms
from .models import Patient, Visit, Appointment
from doctors.models import Procedure, Doctor
from clinics.models import Clinic
from phonenumber_field.formfields import PhoneNumberField

class PatientForm(forms.ModelForm):
    d_o_b = forms.DateField(widget=(forms.DateInput(attrs={'type':'date'})), label="Date of Birth")
    ssn_last_4 = forms.CharField(widget=(forms.NumberInput), label="SSN last four digits")
    phone_number = PhoneNumberField(region="CA")
    # gender = forms.ModelChoiceField(widget=(forms.Select),empty_label=('select gender'), label=('Gender'))

    class Meta:
        model = Patient
        fields = ['name', 'd_o_b', 'phone_number', 'address', 'gender', 'ssn_last_4']

class VisitForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), widget=(forms.Select),empty_label=('select patient'), label=('Patients Name'))
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), widget=(forms.Select),empty_label=('select doctor'), label=('Doctors Name'))
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all(), widget=(forms.Select),empty_label=('select clinic'), label=('Clinics Name'))
    visit_date = forms.DateField(widget=(forms.DateInput(attrs={'type':'date'})), label=('Day of Visit'))
    visit_time = forms.TimeField(widget=(forms.TimeInput(attrs={'type':'time'})), label=('Time of Visit'))
    procedures = forms.ModelMultipleChoiceField(queryset=Procedure.objects.all(), widget=(forms.CheckboxSelectMultiple), label=('Procedures Done'))
    doctors_notes = forms.CharField(widget=(forms.Textarea))

    class Meta:
        model=Visit
        fields = ['patient', 'visit_date', 'visit_time', 'doctor', 'clinic', 'procedures', 'doctors_notes']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['patient'].initial = 1
class AppointmentForm(forms.ModelForm):
    last_visit_date = forms.DateField(widget=(forms.DateInput))
    next_appointment_date = forms.DateField(widget=(forms.DateInput))
    next_appointment_procedure = forms.CharField(widget=(forms.Textarea))

    class Meta:
        model = Appointment 
        fields = ['patient', 'last_visit_date', 'last_visit_time', 'last_visit_doctor', 'last_visit_procedures', 'next_appointment', 'next_appointment_date', 'next_appointment_time', 'next_appointment_doctor', 'next_appointment_procedure']


class ScheduleAppointmentForm(forms.Form):
    procedure = forms.CharField()
    clinic = forms.IntegerField()
    doctor = forms.IntegerField()
    time_slot = forms.IntegerField()