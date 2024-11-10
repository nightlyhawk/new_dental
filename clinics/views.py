from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.views.generic import ListView, DetailView
from django.http.response import JsonResponse
from .models import Clinic
from .forms import ClinicForm
from doctors.models import Doctor, Procedure

# Create your views here.
class ClinicListView(ListView):
    model = Clinic
    context_object_name = 'clinics'
    template_name = "clinics_list.html"


def clinic_create(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST)
        if form.is_valid():
            form.save()
            return  redirect('clinic_detail.html', form.cleaned_data['id'])
    else:
        form = ClinicForm()
    return render(request, 'clinic_create.html', {'form': form})


def clinic_update(request, pk):
    clinic = Clinic.objects.get(id=pk)
    if request.method == 'POST':
        form = ClinicForm(request.POST, instance=clinic)
        if form.is_valid():
            form.save()
            return  redirect('clinic_update.html', clinic.pk)
    else:
        form = ClinicForm(instance=clinic)
    return render(request, 'clinic_update.html', {'form': form})

class ClinicDetailView(DetailView):
    model = Clinic
    context_object_name = 'clinic'
    template_name = "clinic_detail.html"
    
    def get_queryset(self):
        self.clinic = get_object_or_404(Clinic, id=self.kwargs["pk"])
        return self.clinic

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["doctors"] = Doctor.objects.filter(clinic=self.clinic)
    #     return context

def add_doctor(request, pk, dpk):
    if request.method == 'POST':
        clinic = Clinic.objects.get(id=pk)
        doctor = Doctor.objects.get(id=pk)
        clinic.doctors.add(doctor)
        clinic.save(update_fields=('doctors'))
        return render(request, 'clinic_detail.html', {})
    else:
        doctors = Doctor.objects.all()
        return render(request, 'add_affiliate.html', {'doctors': doctors})

def retrieve_working_doctors(request, pk):
    doctors = Clinic.objects.get(id=pk).doctors.all()
    data = [
        {
            'id': doctor.pk,
            'name': doctor.name
        }
        for doctor in doctors.all()
    ]
    return JsonResponse({"doctors": data})

def clinic_procedure_doctors(request, pk):
    clinics = Clinic.objects.filter(doctors__specialties__id=pk)
    data = [
        {
            'id': clinic.pk,
            'name': clinic.name
        }
        for clinic in clinics
    ]
    return JsonResponse({"clinics": data})