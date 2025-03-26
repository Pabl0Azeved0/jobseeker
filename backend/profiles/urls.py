from django.urls import path
from .views import ProfileListCreateView, ProfileDetailView, ProfileSearchView, MyProfileView

urlpatterns = [
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<uuid:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/search/', ProfileSearchView.as_view(), name='profile-search'),
    path('profiles/me/', MyProfileView.as_view(), name='my-profile'),
]
