from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from jobs.models import Job
from .models import Application

User = get_user_model()

class ApplicationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('applicant', password='testpass')
        self.job = Job.objects.create(
            title='Developer', description='Test', location='Remote',
            salary=50000, posted_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_application(self):
        response = self.client.post('/api/applications/', {
            'job_id': self.job.id,
            'cover_letter': 'I am interested.'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['cover_letter'], 'I am interested.')
        self.assertEqual(response.data['job']['id'], str(self.job.id))
        self.assertEqual(response.data['status'], 'applied')

    def test_get_application(self):
        app = Application.objects.create(
            job=self.job, applicant=self.user, cover_letter='Test letter'
        )
        response = self.client.get(f'/api/applications/{app.id}/')
        self.assertEqual(response.status_code, 200)
