import pytest
from django.urls import reverse
from django.core import mail
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from jobs.models import Job
from .models import Application

pytestmark = pytest.mark.django_db

User = get_user_model()

# --- Fixtures ---

@pytest.fixture
def api_client():
    """A fixture to provide an API client."""
    return APIClient()

@pytest.fixture
def applicant_user():
    """Fixture for a user who applies for jobs."""
    return User.objects.create_user(username='applicant', email='applicant@example.com', password='password123', role='seeker')

@pytest.fixture
def recruiter_user():
    """Fixture for a user who posts jobs."""
    return User.objects.create_user(username='recruiter', email='recruiter@example.com', password='password123', role='recruiter')

@pytest.fixture
def test_job(recruiter_user):
    """Fixture for a job posting."""
    return Job.objects.create(
        title='Software Engineer',
        description='Build amazing things.',
        location='Remote',
        salary=120000,
        posted_by=recruiter_user
    )

# --- Model and Serializer Tests ---

def test_application_creation(applicant_user, test_job):
    """Test creating an Application model instance."""
    app = Application.objects.create(
        job=test_job,
        applicant=applicant_user,
        cover_letter="I'm a great fit!"
    )
    assert app.status == 'applied'
    assert str(app) == f"{applicant_user.username} - {test_job.title}"

def test_duplicate_application_fails_at_db_level(applicant_user, test_job):
    """Test the unique_together constraint on the model."""
    Application.objects.create(job=test_job, applicant=applicant_user)
    from django.db import IntegrityError
    with pytest.raises(IntegrityError):
        Application.objects.create(job=test_job, applicant=applicant_user)
