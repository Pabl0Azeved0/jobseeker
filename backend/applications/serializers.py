from rest_framework import serializers
from .models import Application
from jobs.models import Job
from jobs.serializers import JobSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), write_only=True, source='job'
    )

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_id', 'applicant', 'status', 'applied_at', 'cover_letter']
        read_only_fields = ['id', 'applicant', 'applied_at', 'job']
