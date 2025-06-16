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


# --- View Tests: MyProfileView ---

class TestMyProfileView:
    def test_get_my_profile_creates_if_not_exists(self, api_client, seeker_user):
        """Test GET /profiles/me/ when no profile exists yet; it should be created."""
        api_client.force_authenticate(user=seeker_user)
        url = reverse('my-profile')
        
        assert not Profile.objects.filter(user=seeker_user).exists()
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert Profile.objects.filter(user=seeker_user).exists()
        assert response.data['user'] == seeker_user.id

    def test_update_my_profile(self, api_client, seeker_user):
        """Test that a user can update their own profile via PATCH."""
        api_client.force_authenticate(user=seeker_user)
        # First, ensure the profile exists by calling the endpoint
        url = reverse('my-profile')
        api_client.get(url) 

        data = {'bio': 'I am a skilled developer.', 'location': 'Brazil'}
        response = api_client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['bio'] == 'I am a skilled developer.'
        seeker_user.profile.refresh_from_db()
        assert seeker_user.profile.location == 'Brazil'

    def test_upload_resume_to_my_profile(self, api_client, seeker_user):
        """Test uploading a file to the resume field."""
        api_client.force_authenticate(user=seeker_user)
        url = reverse('my-profile')

        # Create a dummy file in memory for the upload
        resume_file = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        data = {'resume': resume_file}
        
        response = api_client.patch(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'resumes/resume.pdf' in response.data['resume']
        
        # Clean up the created file after the test
        seeker_user.profile.refresh_from_db()
        seeker_user.profile.resume.delete(save=True)
