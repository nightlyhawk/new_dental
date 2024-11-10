from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http.response import JsonResponse
from .models import Clinic
from .forms import ClinicForm
from doctors.models import Doctor
from patients.models import Visit
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ClinicListView(ListView):
    model = Clinic
    context_object_name = 'clinics'
    template_name = "clinics_list.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        patients_count = (
            Visit.objects.values('clinic')
            .annotate(total_patients=Count('patient', distinct=True))
        )
        context['no_of_affiliated_patients'] = {item['clinic']: item['total_patients'] for item in patients_count}     
        return context


def clinic_create(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated():
                return  redirect('clinic_detail.html', form.cleaned_data['id'])
            return render(request, 'success.hrml', {'action_text': 'register another clinic?', 'action_url': 'clinics_urls:create-clinic'})
    else:
        form = ClinicForm()
    return render(request, 'clinic_create.html', {'form': form})

@login_required
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

class ClinicDetailView(LoginRequiredMixin, DetailView):
    model = Clinic
    context_object_name = 'clinic'
    template_name = "clinic_detail.html"
    
    def get_object(self):
        self.clinic = Clinic.objects.get(id=self.kwargs["pk"])
        return self.clinic

@login_required
def add_doctor(request, pk, dpk=None):
    dpk = request.query_params.get('dpk', None)
    if request.method == 'POST':
        clinic = Clinic.objects.get(id=pk)
        doctor = Doctor.objects.get(id=dpk)
        clinic.doctors.add(doctor)
        clinic.save(update_fields=('doctors'))
        return render(request, 'clinic_detail.html', {})
    else:
        doctors = Doctor.objects.all()
        return render(request, 'add_doctor.html', {'doctors': doctors})

@login_required
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

@login_required
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