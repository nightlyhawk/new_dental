from django import forms
from .models import Clinic
from doctors.models import Doctor

class ClinicForm(forms.ModelForm):
    phone_number = forms.CharField(widget=(forms.TextInput(attrs={'type': 'tel'})))
    doctors = forms.ModelChoiceField(queryset=Doctor.objects.all(), widget=(forms.CheckboxSelectMultiple), label=('Doctors'))
    class Meta:
        model = Clinic
        fields = ['name', 'phone_number', 'city', 'state', 'doctors']
    
    
    
    