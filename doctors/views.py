from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Doctor, Schedule, Procedure
from patients.models import Patient, Visit
from clinics.models import Clinic
from .forms import DoctorForm, ScheduleForm
from django.db.models import Count
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    context_object_name = 'doctors'
    template_name = "doctors_list.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #both in appointmnt add to list and return
        # doctors = self.object_list
        patients_count = (
            Visit.objects.values('doctor')
            .annotate(total_patients=Count('patient', distinct=True))
        )
        
        # Calculate the number of unique clinics for each doctor
        # clinics_count = (
        #     Appointment.objects.values('doctor')
        #     .annotate(total_clinics=Count('clinic', distinct=True))
        # )
        # no_of_patients_clinics = doctors.values('doctor_appointments').annotate(total=Count('id'))
        # context['no_of_affiliated_patients'] = no_of_patients_clinics
        # context['no_of_affiliated_clinics'] = no_of_patients_clinics
        context['no_of_affiliated_patients'] = {item['doctor']: item['total_patients'] for item in patients_count}
        # context['no_of_affiliated_clinics'] = {item['doctor']: item['total_clinics'] for item in clinics_count}
        return context
    
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated():
                return  redirect('doctor_detail.html', form.cleaned_data['id'])
            return render(request, 'success.hrml', {'action_text': 'create another doctor record?', 'action_url': 'doctors_urls:create-doctor'})
    else:
        form = DoctorForm()
    return render(request, 'doctor_create.html', {'form': form})

@login_required
def doctor_update(request, pk):
    doctor = Doctor.objects.get(id=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return  redirect('clinics_urls:list-clinics')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctor_create.html', {'form': form})

class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    context_object_name = 'doctor'
    template_name = "doctor_detail.html"
    
    def get_object(self):
        self.doctor = get_object_or_404(Doctor, id=self.kwargs["pk"])
        return self.doctor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['procedures'] = Procedure.objects.all()
        clinic_ids = Visit.objects.filter(doctor=self.doctor).values_list('clinic', flat=True).distinct()
        context["clinics"] = Clinic.objects.filter(id__in=clinic_ids)
        patient_ids = Visit.objects.filter(doctor=self.doctor).values_list('patient', flat=True).distinct()
        context["patients"] = Patient.objects.filter(id__in=patient_ids)
        print(context['patients'])
        return context
    
@login_required
def schedule_update(request, pk):
    schedule = Schedule.objects.get(id=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return  redirect('clinic_urls:list-clinics')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'schedule_update.html', {'form': form})

@login_required
def get_schedule(request, pk):
    schedules = Doctor.objects.get(id=pk).schedule.all()
    data = [
        {
            "id": schedule.pk,
            "startTime": schedule.startTime,
            "endTime": schedule.endTime
        }
        for schedule in schedules
        ]
    return JsonResponse({"schedules": data})