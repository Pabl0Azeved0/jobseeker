import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    ROLE_CHOICES = (
        ("seeker", "Job Seeker"),
        ("recruiter", "Recruiter"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="seeker")

    def __str__(self):
        return f"{self.username} ({self.role})"
