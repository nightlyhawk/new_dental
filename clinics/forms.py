from django import forms
from .models import Clinic
from doctors.models import Doctor
from phonenumber_field.formfields import PhoneNumberField

class ClinicForm(forms.ModelForm):
    phone_number = PhoneNumberField(region="CA")
    doctors = forms.ModelChoiceField(queryset=Doctor.objects.all(), widget=(forms.CheckboxSelectMultiple), label=('Doctors'))
    class Meta:
        model = Clinic
        fields = ['name', 'phone_number', 'city', 'state', 'doctors']
    
    
    
    