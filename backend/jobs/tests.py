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


# --- Model and Serializer Tests ---

def test_job_model_str(test_job):
    """Test the model's __str__ representation."""
    assert str(test_job) == 'Backend Developer'

def test_job_serializer_invalid_salary():
    """Test that the serializer rejects a negative salary."""
    from .serializers import JobSerializer
    data = {'title': 'Valid Title', 'description': 'desc', 'location': 'loc', 'salary': -500}
    serializer = JobSerializer(data=data)
    assert not serializer.is_valid()
    assert 'salary' in serializer.errors

def test_job_serializer_invalid_title():
    """Test that the serializer rejects a short title."""
    from .serializers import JobSerializer
    data = {'title': 'A', 'description': 'desc', 'location': 'loc', 'salary': 50000}
    serializer = JobSerializer(data=data)
    assert not serializer.is_valid()
    assert 'title' in serializer.errors


# --- View Tests: List and Create ---

class TestJobListCreateView:
    def test_list_jobs_unauthenticated(self, api_client, test_job):
        """Unauthenticated users should be able to list jobs."""
        url = reverse('job-list-create')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_create_job_as_recruiter_success(self, api_client, recruiter_user):
        """A logged-in recruiter should be able to create a job."""
        api_client.force_authenticate(user=recruiter_user)
        url = reverse('job-list-create')
        data = {'title': 'Python Dev', 'description': 'desc', 'location': 'Porto', 'salary': 55000}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['posted_by'] == recruiter_user.id
        
    def test_create_job_as_seeker_fail(self, api_client, seeker_user):
        """A job seeker should NOT be able to create a job."""
        api_client.force_authenticate(user=seeker_user)
        url = reverse('job-list-create')
        data = {'title': 'Job I Want', 'description': 'desc', 'location': 'loc'}
        response = api_client.post(url, data)
        # This will be Forbidden because of IsAdminUser permission
        assert response.status_code == status.HTTP_403_FORBIDDEN
