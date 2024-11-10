from django.urls import path
from .views import DoctorListView, DoctorDetailView, doctor_create, doctor_update, schedule_update, get_schedule

app_name = 'doctors_urls'

urlpatterns = [
    path("list/", DoctorListView.as_view(), name='list-doctors'),
    path("detail/<int:pk>/", DoctorDetailView.as_view(), name='detail-doctor'),
    path("create/", doctor_create, name='create-doctor'),
    path("update/", doctor_update, name='update-doctor'),
    path("edit/schedule/", schedule_update, name='update-schedule'),
    path("retrieve/schedule/<int:pk>/", get_schedule, name='retrieve-schedule'),
]