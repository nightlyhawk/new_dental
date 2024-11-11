from django import forms
from .models import Doctor, Schedule, Procedure
from phonenumber_field.formfields import PhoneNumberField

class DoctorForm(forms.ModelForm):
    npi = forms.CharField(widget=(forms.TextInput), label=('NPI (National Provider Identifier)'))
    specialties = forms.ModelMultipleChoiceField(queryset=Procedure.objects.all(), widget=(forms.CheckboxSelectMultiple))
    phone_number = PhoneNumberField(region="CA")
    class Meta:
        model = Doctor
        fields = ['name', 'npi', 'email', 'phone_number', 'office_address', 'specialties']

class ScheduleForm(forms.ModelForm):
    startTime = forms.TimeField(widget=(forms.TimeInput))
    endTime = forms.TimeField(widget=(forms.TimeInput))
    
    class Meta:
        model = Schedule
        fields = ['doctor', 'day', 'startTime', 'endTime']