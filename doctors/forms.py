from django import forms
from .models import Doctor, Schedule


class DoctorForm(forms.ModelForm):
    npi = forms.CharField(widget=(forms.TextInput), label=('NPI (National Provider Identifier)'))
    class Meta:
        model = Doctor
        fields = ['name', 'npi', 'office_address', 'specialties']

class ScheduleForm(forms.ModelForm):
    startTime = forms.TimeField(widget=(forms.TimeInput))
    endTime = forms.TimeField(widget=(forms.TimeInput))
    
    class Meta:
        model = Schedule
        fields = ['doctor', 'day', 'startTime', 'endTime']