from typing import Any
import datetime
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Patient, Visit, Appointment
from .forms import PatientForm, AppointmentForm, VisitForm, ScheduleAppointmentForm
from clinics.models import Clinic
from doctors.models import Procedure, Schedule, Doctor
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = "patients_list.html"

    def get_queryset(self):
        return Patient.objects.prefetch_related('patient_appointment').all()


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = "patient_detail.html"

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        self.patient = Patient.objects.prefetch_related('patient_visits', 'patient_appointment').get(pk=pk)
        return self.patient

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = Appointment.objects.get(patient=self.patient)
        context["appointment"] = appointment
        return context

@login_required
def add_visit(request, pk):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_urls:list-patients')
    else:
        initial_data = {'patient': pk}
        form = VisitForm(initial=initial_data)
    return render(request, 'visit.html', {'form': form, 'id': pk})



def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                return redirect("patients_urls:list-patients")
            return render(request, 'success.html', {'action_text': 'create another patient record?', 'action_url': 'patients_urls:add-patient'})
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {'form': form})

@login_required
def update_patient(request, pk):
    if request.method == 'POST':
        patient = Patient.objects.get(id=pk)
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patients_urls:list-patients")
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {'form': form})

@login_required
def schedule_appointment(request, pk):
    if request.method == 'POST':
        form = ScheduleAppointmentForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(id=pk)
            procedure = Procedure.objects.get(id=form.cleaned_data['procedure'])
            # clinic = Clinic.objects.get(id=form.cleaned_data['clinic'])
            doctor = Doctor.objects.get(id=form.cleaned_data['doctor'])
            time_slot = form.cleaned_data['time_slot']
            appointment, created = Appointment.objects.get_or_create(patient=patient)
            appointment.last_visit_date = appointment.next_appointment_date
            appointment.last_visit_doctor = appointment.last_visit_doctor
            appointment.last_visit_procedures.add(appointment.next_appointment_procedure)
            appointment.last_visit_time = appointment.next_appointment_time
            appointment.next_appointment = True
            day = Schedule.objects.get(id=time_slot).day
            fulldate = datetime.datetime.now()
            today = fulldate.day
            day_name = fulldate.weekday()
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if day_name == days.index(day):
                date = datetime.datetime(fulldate.year, datetime.datetime.month, day)
            elif day_name < days.index(day):
                day= today + 1 + days.index(day) + 1
                date = datetime.datetime(fulldate.year, fulldate.month, day)
            elif day_name > days.index(day):
                day= today + len(days) + days.index(day) + 1
                date = datetime.datetime(fulldate.year, fulldate.month, day)
            time = datetime.time(time_slot)
            appointment.next_appointment_date = date
            appointment.next_appointment_doctor = doctor
            appointment.next_appointment_procedure = procedure
            appointment.next_appointment_time = time
            appointment.save()
            return redirect("patients_urls:list-patients")
    else:
        patient = Patient.objects.get(id=pk)
        procedures = Procedure.objects.all()
    return render(request, 'schedule_appt.html', {'procedures': procedures, 'patient': patient})