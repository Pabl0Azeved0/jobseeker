from django.urls import path
from .views import SignupView, UserListView, UserDetailView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<uuid:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("signup/", SignupView.as_view(), name="signup"),
]
