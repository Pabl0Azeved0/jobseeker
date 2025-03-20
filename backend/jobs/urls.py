from django.urls import path
from .views import JobListCreateView, JobDetailView, JobSearchView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<uuid:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/search/', JobSearchView.as_view(), name='job-search'),
]
