from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "bio",
            "skills",
            "contact",
            "resume",
            "location",
            "birth_date",
        ]
        read_only_fields = ["id", "user"]

    def validate(self, attrs):
        for field in ["bio", "skills", "contact", "location"]:
            if attrs.get(field) is None:
                attrs[field] = ""
        return attrs
