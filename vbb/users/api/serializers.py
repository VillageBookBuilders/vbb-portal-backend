from contextlib import suppress

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from vbb.profiles.serializers import AdvisorProfileSerializer, MentorProfileSerializer, LibrarianProfileSerializer, StudentProfileSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    mentor_profile = serializers.SerializerMethodField()
    student_profile = serializers.SerializerMethodField()
    librarian_profile = serializers.SerializerMethodField()
    advisor_profile = serializers.SerializerMethodField()

    def get_mentor_profile(self, user):
        with suppress(ObjectDoesNotExist):
            return MentorProfileSerializer(user.mentorprofile).data

    def get_student_profile(self, user):
        with suppress(ObjectDoesNotExist):
            return StudentProfileSerializer(user.studentprofile).data

    def get_librarian_profile(self, user):
        with suppress(ObjectDoesNotExist):
            return LibrarianProfileSerializer(user.librarianprofile).data

    def get_advisor_profile(self, user):
        with suppress(ObjectDoesNotExist):
            return AdvisorProfileSerializer(user.advisorprofile).data


    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "name",
            "first_name",
            "last_name",
            "profileImage",
            "email",
            "time_zone",
            "role",
            "is_student",
            "is_librarian",
            "is_mentor",
            "mentor_profile",
            "student_profile",
            "librarian_profile",
            "advisor_profile",
            "date_of_birth",
            "gender",
            "has_dropped_out",
            "drop_out_date",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
