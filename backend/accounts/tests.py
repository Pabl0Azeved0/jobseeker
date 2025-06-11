import pytest
from django.urls import reverse
from django.core import mail
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSignupSerializer
from .permissions import IsRecruiter, IsAdmin

# Using pytest.mark.django_db allows tests to access the database.
pytestmark = pytest.mark.django_db

User = get_user_model()

# --- Fixtures ---
# Fixtures are reusable components for your tests.

@pytest.fixture
def api_client():
    """A fixture to provide an API client."""
    return APIClient()

@pytest.fixture
def seeker_user():
    """A fixture to create a user with the 'seeker' role."""
    return User.objects.create_user(username='seeker', email='seeker@example.com', password='password123', role='seeker')

@pytest.fixture
def recruiter_user():
    """A fixture to create a user with the 'recruiter' role."""
    return User.objects.create_user(username='recruiter', email='recruiter@example.com', password='password123', role='recruiter')

@pytest.fixture
def admin_user():
    """A fixture to create a user with the 'admin' role."""
    return User.objects.create_user(username='admin', email='admin@example.com', password='password123', role='admin')

