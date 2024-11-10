from django import forms
from .models import Clinic


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'phone_number', 'city', 'state', 'doctors']
    
    
    
    