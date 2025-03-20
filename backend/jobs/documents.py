from django_elasticsearch_dsl import Document, Index, fields
from .models import Job

job_index = Index('jobs')

@job_index.doc_type
class JobDocument(Document):
    posted_by = fields.ObjectField(properties={
        'id': fields.TextField(),
        'username': fields.TextField(),
        'email': fields.TextField(),
    })

    class Django:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'location',
            'salary',
            'created_at',
        ]
