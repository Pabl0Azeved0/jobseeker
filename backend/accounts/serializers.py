from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from accounts.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]
        read_only_fields = ["id", "username", "email", "role"]


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default="seeker")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "password2", "role")

    def validate_email(self, value):
        validate_email(value)
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must have at least 3 characters."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data.get("role", "seeker"),
        )
        return user
