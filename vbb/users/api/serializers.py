from django.contrib.auth import get_user_model
from rest_framework import serializers
import django.contrib.auth.password_validation as validators

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "email", "time_zone"]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "username"}}


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, write_only=True)

    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except validators.ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"]
        )
        return user

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
