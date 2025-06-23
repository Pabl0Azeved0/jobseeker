from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_elasticsearch_dsl.search import Search
from .models import Profile
from .serializers import ProfileSerializer


class ProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class ProfileSearchView(APIView):

    def get(self, request):
        query = request.query_params.get("q", "")
        s = Search(index="profiles").query(
            "multi_match", query=query, fields=["bio", "user.username", "user.email"]
        )
        response = s.execute()
        results = [
            {
                "id": hit.id,
                "bio": hit.bio,
                "username": hit.user.username,
                "email": hit.user.email,
            }
            for hit in response
        ]
        return Response(results)


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
