from contextlib import suppress

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from vbb.profiles.serializers import MentorProfileSerializer, StudentProfileSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    mentor_profile = serializers.SerializerMethodField()
    student_profile = serializers.SerializerMethodField()

    def get_mentor_profile(self, user):
        with suppress(ObjectDoesNotExist):
            return MentorProfileSerializer(user.mentorprofile).data

    def get_student_profile(self, user):
        with suppress(ObjectDoesNotExist):
            return StudentProfileSerializer(user.studentprofile).data

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "email",
            "time_zone",
            "is_student",
            "is_librarian",
            "is_mentor",
            "mentor_profile",
            "student_profile",
            "date_of_birth",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
