import uuid
from django.db import models
from django.conf import settings
from jobs.models import Job


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("applied", "Applied"),
            ("viewed", "Viewed"),
            ("rejected", "Rejected"),
            ("accepted", "Accepted"),
        ],
        default="applied",
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

    class Meta:
        unique_together = ("job", "applicant")
