from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime
from .models import Clinic
from doctors.models import Doctor, Procedure
from patients.models import Visit, Patient


# Create your tests here.
User = get_user_model()

class ClinicViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test@user.com', password='testpassword')
        self.client.login(email='test@user.com', password='testpassword')

        # Sample data setup
        self.clinic = Clinic.objects.create(name="Sample Clinic", phone_number="+1 604 401 1234", city='Here', state='there')
        self.doctor = Doctor.objects.create(npi=111111, name="Sample Doctor", email='brightsmile@gmail.com', phone_number="+1 604 401 1234", office_address='somewhere')
        self.patient = Patient.objects.create(name='Patient name', d_o_b=datetime.datetime.date(), address='soemwhere', gender='M', phone_number="+1 604 401 1234", ssn_last_4=4444)
        Visit.objects.create(clinic=self.clinic, patient=self.patient, visit_date=datetime.datetime.date() , visit_time=datetime.datetime.time(), doctors_notes='gargle')

    def test_clinic_list_view(self):
        url = reverse('clinics_urls:list-clinics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinics_list.html")
        self.assertIn('clinics', response.context)
        self.assertIn('no_of_affiliated_patients', response.context)

    def test_clinic_detail_view(self):
        url = reverse('clinics_urls:detail-clinic', kwargs={'pk': self.clinic.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic_detail.html")
        self.assertEqual(response.context['clinic'], self.clinic)

    def test_clinic_create_view_post(self):
        url = reverse('clinics_urls:create-clinic')
        response = self.client.post(url, {'name': 'New Clinic', 'phone_number':"+1 604 401 1234", 'city':'Here', 'state':'there'})
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Clinic.objects.filter(name="New Clinic").exists())

    def test_clinic_update_view(self):
        url = reverse('clinics_urls:update-clinic', kwargs={'pk': self.clinic.pk})
        response = self.client.post(url, {'name': 'Updated Clinic Name'})
        self.assertEqual(response.status_code, 302) 
        self.clinic.refresh_from_db()
        self.assertEqual(self.clinic.name, 'Updated Clinic Name')

    def test_add_doctor_view(self):
        url = reverse('clinics_urls:add-doctor', kwargs={'pk': self.clinic.pk})
        response = self.client.post(url, {'dpk': self.doctor.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.doctor, self.clinic.doctors.all())

    def test_retrieve_working_doctors_view(self):
        self.clinic.doctors.add(self.doctor)
        url = reverse('clinics_urls:retrieve-doctor', kwargs={'pk': self.clinic.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["doctors"][0]["name"], self.doctor.name)

    def test_clinic_procedure_doctors_view(self):
        specialty = Procedure.objects.create(name="Sample Specialty")
        self.doctor.specialties.add(specialty)
        self.clinic.doctors.add(self.doctor)

        url = reverse('clinics_urls:retrieve-clinics-by-procedure', kwargs={'pk': specialty.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["clinics"][0]["name"], self.clinic.name)
