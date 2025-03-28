from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.management import call_command
from .models import Job

User = get_user_model()

class JobAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='recruiter')  # <-- FIX: role='recruiter'
        self.client.force_authenticate(user=self.user)

    def test_job_creation(self):
        data = {
            'title': 'New Job',
            'description': 'Job description',
            'location': 'Remote',
            'salary': '70000'
        }
        response = self.client.post('/api/jobs/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['posted_by'], self.user.id)

    def test_job_list(self):
        Job.objects.create(
            title='Job 1',
            description='Description',
            location='Remote',
            salary=50000,
            posted_by=self.user
        )
        response = self.client.get('/api/jobs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_job_detail(self):
        job = Job.objects.create(
            title='Detailed Job',
            description='Detailed description',
            location='Remote',
            salary=50000,
            posted_by=self.user
        )
        response = self.client.get(f'/api/jobs/{job.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], job.title)

    def test_job_search(self):
        Job.objects.create(
            title='Elasticsearch Developer',
            description='Developing with Elasticsearch',
            location='Remote',
            salary=80000,
            posted_by=self.user
        )

        call_command('search_index', '--rebuild', '-f')

        response = self.client.get('/api/jobs/search/?q=Elasticsearch')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Elasticsearch Developer')
