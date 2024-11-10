from django import forms
from .models import Doctor, Schedule, Procedure


class DoctorForm(forms.ModelForm):
    npi = forms.CharField(widget=(forms.TextInput), label=('NPI (National Provider Identifier)'))
    specialties = forms.ModelMultipleChoiceField(queryset=Procedure.objects.all(), widget=(forms.CheckboxSelectMultiple))
    phone_number = forms.CharField(widget=(forms.TextInput(attrs={'type': 'tel'})))
    class Meta:
        model = Doctor
        fields = ['name', 'npi', 'email', 'phone_number', 'office_address', 'specialties']

class ScheduleForm(forms.ModelForm):
    startTime = forms.TimeField(widget=(forms.TimeInput))
    endTime = forms.TimeField(widget=(forms.TimeInput))
    
    class Meta:
        model = Schedule
        fields = ['doctor', 'day', 'startTime', 'endTime']