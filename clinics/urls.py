from django.urls import path
from .views import ClinicListView, ClinicDetailView, clinic_create, clinic_update, add_doctor, retrieve_working_doctors, clinic_procedure_doctors, remove_doctor

app_name = 'clinics_urls'

urlpatterns = [
    path("list/", ClinicListView.as_view(), name='list-clinics'),
    path("detail/<int:pk>/", ClinicDetailView.as_view(), name='detail-clinic'),
    path("create/", clinic_create, name='create-clinic'),
    path("update/", clinic_update, name='update-clinic'),
    path("add/doctor/<int:pk>/", add_doctor, name='add-doctor'),
    path("remove/doctor/<int:pk>/", remove_doctor, name='remove-doctor'),
    path("retrieve/doctors/<int:pk>/", retrieve_working_doctors, name='retrieve-doctor'),
    path("retrieve/clinics/by/procedure/<int:pk>/", clinic_procedure_doctors, name='retrieve-clinics-by-procedure'),
]