from rest_framework import generics, permissions
from .models import Application
from .serializers import ApplicationSerializer
from django.core.mail import send_mail
from django.conf import settings

class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        application = serializer.save(applicant=self.request.user)
        job_owner_email = application.job.posted_by.email
        send_mail(
            'New Job Application Received',
            f"Hello,\n\n{self.request.user.username} has applied for your job posting '{application.job.title}'.",
            settings.DEFAULT_FROM_EMAIL,
            [job_owner_email],
            fail_silently=False,
        )

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        This ensures the user can only see/edit/delete their own applications.
        """
        return Application.objects.filter(applicant=self.request.user)
