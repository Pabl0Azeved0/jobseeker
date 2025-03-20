from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_elasticsearch_dsl.search import Search
from .models import Job
from .serializers import JobSerializer


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class JobSearchView(APIView):

    def get(self, request):
        query = request.query_params.get('q', '')
        s = Search(index='jobs').query(
            'multi_match', query=query, fields=['title', 'description', 'location']
        )
        response = s.execute()
        results = [
            {
                'id': hit.id,
                'title': hit.title,
                'description': hit.description,
                'location': hit.location,
                'salary': hit.salary
            } for hit in response
        ]
        return Response(results)
