from django.urls import path
from .views import PatientListView, PatientDetailView, add_visit, add_patient, schedule_appointment, update_patient

app_name = 'patients_urls'

urlpatterns = [
    path("list/", PatientListView.as_view(), name='list-patients'),
    path("detail/<int:pk>/", PatientDetailView.as_view(), name='detail-patients'),
    path("visit/add/<int:pk>/", add_visit, name='visit-add-patients'),
    path("add/", add_patient, name='add-patients'),
    path("edit/<int:pk>/", update_patient, name='edit-patients'),
    path("schedule/appointment/<int:pk>/", schedule_appointment, name='schedule-appointment'),
]