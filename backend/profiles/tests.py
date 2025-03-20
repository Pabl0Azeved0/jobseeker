from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.management import call_command
from .models import Profile

User = get_user_model()

class ProfileAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('profileuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_profile(self):
        data = {'bio': 'Hello World'}
        response = self.client.post('/api/profiles/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['bio'], 'Hello World')
        self.assertEqual(response.data['user'], self.user.id)

    def test_get_own_profile_list(self):
        Profile.objects.create(user=self.user, bio='Own bio')
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['bio'], 'Own bio')

    def test_get_profile_detail(self):
        profile = Profile.objects.create(user=self.user, bio='Detailed bio')
        response = self.client.get(f'/api/profiles/{profile.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['bio'], 'Detailed bio')

    def test_profile_access_restricted_to_owner(self):
        other_user = User.objects.create_user('otheruser', password='testpass')
        other_profile = Profile.objects.create(user=other_user, bio='Other bio')
        response = self.client.get(f'/api/profiles/{other_profile.id}/')
        self.assertEqual(response.status_code, 404)

    def test_profile_search(self):
        Profile.objects.create(user=self.user, bio='Expert Python Developer')

        call_command('search_index', '--rebuild', '-f')

        response = self.client.get('/api/profiles/search/?q=Python')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['bio'], 'Expert Python Developer')
