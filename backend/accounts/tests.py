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


# --- Model Tests ---

def test_custom_user_creation():
    """Test that a user can be created with a specific role and has a UUID id."""
    user = User.objects.create_user(username='testuser', email='test@test.com', password='password', role='recruiter')
    assert user.username == 'testuser'
    assert user.role == 'recruiter'
    assert user.id is not None
    assert str(user) == "testuser (recruiter)"

def test_user_default_role():
    """Test that a new user defaults to the 'seeker' role."""
    user = User.objects.create_user(username='defaultuser', email='default@test.com', password='password')
    assert user.role == 'seeker'


# --- Serializer Tests (Signup) ---

def test_signup_serializer_valid():
    """Test the signup serializer with valid data."""
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "StrongPassword123",
        "password2": "StrongPassword123",
        "role": "recruiter"
    }
    # The 'context' is important for some validators
    serializer = UserSignupSerializer(data=data, context={'request': None})
    assert serializer.is_valid(raise_exception=True)
    user = serializer.save()
    assert user.role == 'recruiter'
    assert user.username == 'newuser'

def test_signup_serializer_passwords_mismatch():
    """Test that the serializer raises an error if passwords do not match."""
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "password2": "password456"
    }
    serializer = UserSignupSerializer(data=data)
    assert not serializer.is_valid()
    assert 'password' in serializer.errors
