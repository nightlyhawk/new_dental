from typing import Any
import datetime
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Patient, Visit, Appointment
from .forms import PatientForm, AppointmentForm, VisitForm, ScheduleAppointmentForm
from clinics.models import Clinic
from doctors.models import Procedure, Schedule

# Create your views here.
class PatientListView(ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = "patients_list.html"

    def get_queryset(self):
        # Prefetch related appointments to avoid multiple database queries
        return Patient.objects.prefetch_related('patient_appointment').all()
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     # Aggregate or filter Appointment data by Doctor
    #     appointments = {
    #         apt.patient.pk: apt
    #         for apt in Appointment.objects.all()
    #     }
        
    #     # Add the appointments dictionary to context
    #     context['appointments'] = appointments
    #     return context


class PatientDetailView(DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = "patient_detail.html"

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_patient = Patient.objects.get(pk=pk)
        return view_patient

    # def get_queryset(self) -> QuerySet[Any]:
    #     return super(PatientDetailView).get_queryset()(self)

    # def get_queryset(self):
    #     self.publisher = get_object_or_404(Publisher, name=self.kwargs["publisher"])
    #     return Book.objects.filter(publisher=self.publisher)
    
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     visits = Visit.objects.all()
    #     context["visits"] = []
    #     return context

def add_visit(request, pk):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_url:list-patients', form.cleaned_data['id'])
    else:
        patient = Patient.objects.get(id=pk)
        form = VisitForm()
    return render(request, 'schedule_appt.html', {'form': form, 'patient': patient})


def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("patients_urls:list-patients")
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {'form': form})


def schedule_appointment(request, pk):
    if request.method == 'POST':
        form = ScheduleAppointmentForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(id=pk)
            procedure = form.cleaned_data['procedure']
            clinic = form.cleaned_data['clinic']
            doctor = form.cleaned_data['doctor']
            time_slot = form.cleaned_data['time_slot']
            appointment, created = Appointment.objects.get_or_create(patient=patient)
            appointment.next_appointment = True
            day = Schedule.objects.get(id=time_slot).day
            today = datetime.datetime.day
            day_name = datetime.datetime.weekday
            days = ['Monday', 'Teusday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if day_name == days.index(day):
                date = datetime.datetime(datetime.date.year, datetime.datetime.month, day)
            else:
                day= day + days.index(day) + 1
                date = datetime.datetime(datetime.date.year, datetime.datetime.month, day)
            appointment.next_appointment_date = date
            appointment.next_appointment_doctor
            appointment.next_appointment_procedure
            appointment.next_appointment_time = time_slot
            return redirect("patients_urls:list-patients")
    else:
        patient = Patient.objects.get(id=pk)
        procedures = Procedure.objects.all()
    return render(request, 'schedule_appt.html', {'procedures': procedures, 'patient': patient})