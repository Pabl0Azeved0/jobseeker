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


# --- View Tests ---

class TestSignupView:
    def test_successful_signup(self, api_client):
        """
        Ensure a user can be created successfully and a profile is created.
        """
        url = reverse('signup')
        data = {
            "username": "signupuser",
            "email": "signup@example.com",
            "password": "StrongPassword123",
            "password2": "StrongPassword123",
            "role": "seeker"
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="signupuser").exists()
        
        # Check that a Profile was created
        user = User.objects.get(username="signupuser")
        assert hasattr(user, 'profile')

    def test_signup_sends_welcome_email(self, api_client):
        """
        Ensure the welcome email is sent after a successful signup.
        """
        url = reverse('signup')
        data = {
            "username": "emailuser",
            "email": "emailuser@example.com",
            "password": "StrongPassword123",
            "password2": "StrongPassword123",
        }
        
        # We use a context manager to check that one email was sent
        api_client.post(url, data)
        
        assert len(mail.outbox) == 1
        sent_email = mail.outbox[0]
        assert sent_email.to == ['emailuser@example.com']
        assert 'Welcome to JobSeeker!' in sent_email.subject

    def test_signup_with_invalid_data(self, api_client):
        """
        Ensure signup fails with invalid data (e.g., short username).
        """
        url = reverse('signup')
        data = {
            "username": "a", # Too short
            "email": "invalid@",
            "password": "123",
            "password2": "123"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUserViews:
    def test_list_users_unauthenticated(self, api_client):
        """Ensure unauthenticated users cannot list users."""
        url = reverse('user-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_users_authenticated(self, api_client, seeker_user):
        """Ensure authenticated users can list users."""
        url = reverse('user-list')
        api_client.force_authenticate(user=seeker_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_user_detail_view(self, api_client, seeker_user, recruiter_user):
        """Ensure authenticated users can view a specific user's details."""
        url = reverse('user-detail', kwargs={'pk': recruiter_user.pk})
        api_client.force_authenticate(user=seeker_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == recruiter_user.username
