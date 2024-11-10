from django.urls import path
from .views import ClinicListView, ClinicDetailView, clinic_create, clinic_update, add_doctor, retrieve_working_doctors, clinic_procedure_doctors

app_name = 'clinics_urls'

urlpatterns = [
    path("list/", ClinicListView.as_view(), name='list-clinics'),
    path("detail/", ClinicDetailView.as_view(), name='detail-doctor'),
    path("create/", clinic_create, name='create-clinic'),
    path("update/", clinic_update, name='update-clinic'),
    path("add/doctor/", add_doctor, name='add-doctor'),
    path("retrieve/doctors/<int:pk>/", retrieve_working_doctors, name='retrieve-doctor'),
    path("retrieve/clinics/by/procedure/<int:pk>/", clinic_procedure_doctors, name='retrieve-clinics-by-procedure'),
]