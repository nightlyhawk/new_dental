from django import forms
from .models import Patient, Visit, Appointment


class PatientForm(forms.ModelForm):
    d_o_b = forms.DateField(widget=(forms.DateInput))
    ssn_last_4 = forms.CharField(widget=(forms.IntegerField))

    class Meta:
        model = Patient
        fields = ['name', 'd_o_b', 'phone_number', 'address', 'gender', 'ssn_last_4']

class VisitForm(forms.ModelForm):
    visit_date_time = forms.DateTimeField(widget=(forms.DateTimeInput))
    doctors_notes = forms.CharField(widget=(forms.Textarea))

    class Meta:
        model=Visit
        fields = ['patient', 'visit_date_time', 'doctor', 'clinic', 'procedures', 'doctors_notes']

class AppointmentForm(forms.ModelForm):
    last_visit_date = forms.DateField(widget=(forms.DateInput))
    next_appointment_date = forms.DateField(widget=(forms.DateInput))
    next_appointment_procedure = forms.CharField(widget=(forms.Textarea))

    class Meta:
        model = Appointment 
        fields = ['patient', 'last_visit_date', 'last_visit_doctor', 'last_visit_procedures', 'next_appointment', 'next_appointment_date', 'next_appointment_doctor', 'next_appointment_procedure']


class ScheduleAppointmentForm(forms.Form):
    procedure = forms.CharField()
    clinic = forms.IntegerField()
    doctor = forms.IntegerField()
    time_slot = forms.IntegerField()