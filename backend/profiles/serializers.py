from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = '__all__'
