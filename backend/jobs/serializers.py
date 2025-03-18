from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'posted_by', 'created_at']

    def validate_salary(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Salary must be positive.")
        return value

    def validate_title(self, value):
        if not value or len(value) < 3:
            raise serializers.ValidationError("Title must have at least 3 characters.")
        return value
