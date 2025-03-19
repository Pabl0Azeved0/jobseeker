from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('profileuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_profile(self):
        response = self.client.post('/api/profiles/', {'bio': 'Hello World'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['bio'], 'Hello World')

    def test_get_profile(self):
        profile = Profile.objects.create(user=self.user, bio='Test bio')
        response = self.client.get(f'/api/profiles/{profile.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['bio'], 'Test bio')
