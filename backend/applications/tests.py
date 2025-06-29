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
    return User.objects.create_user(
        username="applicant",
        email="applicant@example.com",
        password="password123",
        role="seeker",
    )


@pytest.fixture
def recruiter_user():
    """Fixture for a user who posts jobs."""
    return User.objects.create_user(
        username="recruiter",
        email="recruiter@example.com",
        password="password123",
        role="recruiter",
    )


@pytest.fixture
def test_job(recruiter_user):
    """Fixture for a job posting."""
    return Job.objects.create(
        title="Software Engineer",
        description="Build amazing things.",
        location="Remote",
        salary=120000,
        posted_by=recruiter_user,
    )


# --- Model and Serializer Tests ---


def test_application_creation(applicant_user, test_job):
    """Test creating an Application model instance."""
    app = Application.objects.create(
        job=test_job, applicant=applicant_user, cover_letter="I'm a great fit!"
    )
    assert app.status == "applied"
    assert str(app) == f"{applicant_user.username} - {test_job.title}"


def test_duplicate_application_fails_at_db_level(applicant_user, test_job):
    """Test the unique_together constraint on the model."""
    Application.objects.create(job=test_job, applicant=applicant_user)
    from django.db import IntegrityError

    with pytest.raises(IntegrityError):
        Application.objects.create(job=test_job, applicant=applicant_user)


# --- View Tests: List and Create ---


class TestApplicationListCreateView:
    def test_create_application_success(
        self, api_client, applicant_user, test_job, recruiter_user
    ):
        """Ensure an authenticated user can apply for a job."""
        api_client.force_authenticate(user=applicant_user)
        url = reverse("application-list-create")
        data = {
            "job_id": str(test_job.id),
            "cover_letter": "Please consider my application.",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "applied"
        assert response.data["job"]["title"] == test_job.title

        # Check that the email was sent to the recruiter
        assert len(mail.outbox) == 1
        sent_email = mail.outbox[0]
        assert sent_email.to == [recruiter_user.email]
        assert "New Job Application Received" in sent_email.subject

    def test_create_application_unauthenticated(self, api_client, test_job):
        """Ensure unauthenticated users cannot apply."""
        url = reverse("application-list-create")
        data = {"job_id": str(test_job.id)}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_apply_to_same_job_twice(self, api_client, applicant_user, test_job):
        """Ensure the API prevents duplicate applications."""
        api_client.force_authenticate(user=applicant_user)
        url = reverse("application-list-create")
        data = {"job_id": str(test_job.id)}

        # First application should succeed
        response1 = api_client.post(url, data, format="json")
        assert response1.status_code == status.HTTP_201_CREATED

        # Second application should fail with a validation error
        response2 = api_client.post(url, data, format="json")
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "already applied" in response2.data[0]

    def test_list_only_my_applications(
        self, api_client, applicant_user, recruiter_user, test_job
    ):
        """Ensure GET request returns only the user's own applications."""
        # Create an application for the applicant
        Application.objects.create(job=test_job, applicant=applicant_user)
        # Create an application for another user (the recruiter, just for test data)
        Application.objects.create(job=test_job, applicant=recruiter_user)

        api_client.force_authenticate(user=applicant_user)
        url = reverse("application-list-create")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Should only see 1 application, not all 2
        assert len(response.data) == 1
        assert response.data[0]["applicant"]["username"] == applicant_user.username


# --- View Tests: Retrieve, Update, Destroy ---


class TestApplicationDetailView:
    @pytest.fixture
    def user_application(self, applicant_user, test_job):
        """Fixture for an application belonging to the main applicant user."""
        return Application.objects.create(job=test_job, applicant=applicant_user)

    def test_retrieve_own_application(
        self, api_client, applicant_user, user_application
    ):
        """Ensure a user can view their own application."""
        api_client.force_authenticate(user=applicant_user)
        url = reverse("application-detail", kwargs={"pk": user_application.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(user_application.id)

    def test_delete_own_application(self, api_client, applicant_user, user_application):
        """Ensure a user can delete (withdraw) their own application."""
        api_client.force_authenticate(user=applicant_user)
        url = reverse("application-detail", kwargs={"pk": user_application.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Application.objects.filter(pk=user_application.pk).exists()

    # --- Security Test ---
    def test_cannot_view_or_delete_another_users_application(
        self, api_client, recruiter_user, user_application
    ):
        """
        SECURITY: Ensure a user cannot access another user's application details.
        This test checks for a common security flaw.
        """
        # Authenticate as the recruiter, who is NOT the applicant
        api_client.force_authenticate(user=recruiter_user)

        url = reverse("application-detail", kwargs={"pk": user_application.pk})

        # Try to view the application
        get_response = api_client.get(url)
        # If your permissions are not set up correctly, this will return 200 OK.
        # It should return 403 Forbidden or 404 Not Found.
        # Based on your current code, this will likely pass with a 200, revealing a flaw.
        # To fix this, you need to override get_queryset in ApplicationDetailView.
        assert get_response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

        # Try to delete the application
        delete_response = api_client.delete(url)
        assert delete_response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
