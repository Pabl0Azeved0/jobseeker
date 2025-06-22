from django_elasticsearch_dsl import Document, Index, fields
from .models import Profile

profile_index = Index("profiles")


@profile_index.doc_type
class ProfileDocument(Document):
    user = fields.ObjectField(
        properties={
            "id": fields.TextField(),
            "username": fields.TextField(),
            "email": fields.TextField(),
        }
    )

    class Django:
        model = Profile
        fields = [
            "id",
            "bio",
        ]
