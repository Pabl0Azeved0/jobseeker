import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Job
from unittest.mock import MagicMock

# Using pytest.mark.django_db allows tests to access the database.
pytestmark = pytest.mark.django_db

User = get_user_model()

# --- Fixtures ---

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def seeker_user():
    return User.objects.create_user(username='seeker', password='password123', role='seeker')

@pytest.fixture
def recruiter_user():
    return User.objects.create_user(username='recruiter', password='password123', role='recruiter')
    
@pytest.fixture
def admin_user():
    return User.objects.create_user(username='admin', password='password123', role='admin', is_staff=True) # is_staff for IsAdminUser

@pytest.fixture
def test_job(recruiter_user):
    """A job posted by the recruiter user."""
    return Job.objects.create(
        title='Backend Developer',
        description='Develop awesome APIs.',
        location='Lisbon',
        salary=60000.00,
        posted_by=recruiter_user
    )
