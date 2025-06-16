import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile
from unittest.mock import MagicMock

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
def other_user():
    """An additional user for testing access permissions."""
    return User.objects.create_user(username='otheruser', password='password123', role='seeker')


# --- Model and Serializer Tests ---

def test_profile_model_str(seeker_user):
    """Test the model's __str__ representation."""
    profile, _ = Profile.objects.get_or_create(user=seeker_user)
    assert str(profile) == "seeker's Profile"

def test_profile_serializer_none_to_empty_str():
    """Test the custom validate method that converts None to empty strings."""
    from .serializers import ProfileSerializer
    # Data with None values for fields that should be converted
    data = {'bio': None, 'skills': None, 'contact': None, 'location': None}
    serializer = ProfileSerializer(data=data)
    
    # Although the fields are not required, we call is_valid() to trigger validation
    # For a partial update (PATCH), this validation logic is still important.
    # We can simulate this by passing a profile instance.
    profile = Profile()
    serializer = ProfileSerializer(instance=profile, data=data, partial=True)
    
    assert serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    
    # Check that None was converted to ''
    assert validated_data['bio'] == ''
    assert validated_data['skills'] == ''
    assert validated_data['contact'] == ''
    assert validated_data['location'] == ''
