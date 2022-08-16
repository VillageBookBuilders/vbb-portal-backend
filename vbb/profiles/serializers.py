from rest_framework import serializers

from vbb.careers.serializers import CareerSerializer
from vbb.language.serializers import LanguageSerializer
from vbb.libraries.serializers import LibrarySerializer
from vbb.profiles.models import MentorProfile, StudentProfile, AdvisorProfile, LibrarianProfile, Opportunity
from vbb.subjects.serializers import SubjectSerializer, GenreSerializer
from vbb.organizations.serializers import OrganizationSerializer
from vbb.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
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
            "date_of_birth",
            "date_joined",
        ]
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

class UserModelSerializer(serializers.ModelSerializer):
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
            "date_of_birth",
            "date_joined",
        ]
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class OpportunitySerializer(serializers.ModelSerializer):
    """
    Opportunity Serializer
    """

    class Meta:
        model = Opportunity
        fields = '__all__'


class AdvisorProfileSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()

    class Meta:
        model = AdvisorProfile
        fields = '__all__'


class LibrarianProfileSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()

    class Meta:
        model = LibrarianProfile
        fields = '__all__'

class MentorProfileSerializer(serializers.ModelSerializer):
    assigned_library = LibrarySerializer()
    careers = CareerSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    mentoring_languages = LanguageSerializer(many=True)
    opportunities = OpportunitySerializer(many=True)
    organization = OrganizationSerializer(many=False)

    class Meta:
        model = MentorProfile
        fields = [
            "assigned_library",
            "careers",
            "subjects",
            "has_completed_training",
            "interests",
            "phone_number",
            "secondary_email",
            "completed_registration",
            "mentoring_languages",
            "approval_status",
            "is_onboarded",
            "organization",
            "bio",
            "application_video_url",
            "canMeetConsistently",
            "crimesOrMisdemeanor",
            "crimesOrMisdemeanorResponses",
            "meet_provider",
            "opportunities"
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    assigned_library = LibrarySerializer()
    careers_of_interest = CareerSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    mentoring_languages = LanguageSerializer(many=True)
    favorite_genres = GenreSerializer(many=True)

    class Meta:
        model = StudentProfile
        fields = [
            "assigned_library",
            "careers_of_interest",
            "mentoring_languages",
            "subjects",
            "favorite_genres",
            "family_status",
            "family_support_level",
            "graduation_obstacle",
            "grade_level",
            "bio",
            "is_onboarded",
            "is_active",
            "approval_status",
            # the below are fields only for admin level
            # "is_active",
            # "is_verified",
        ]


class MentorProfileWithUserSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    assigned_library = LibrarySerializer()
    careers = CareerSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    mentoring_languages = LanguageSerializer(many=True)
    organization = OrganizationSerializer(many=False)
    opportunities = OpportunitySerializer(many=True)

    class Meta:
        model = MentorProfile
        fields = [
            "user",
            "assigned_library",
            "careers",
            "subjects",
            "has_completed_training",
            "interests",
            "phone_number",
            "secondary_email",
            "completed_registration",
            "mentoring_languages",
            "approval_status",
            "is_onboarded",
            "organization",
            "canMeetConsistently",
            "crimesOrMisdemeanor",
            "crimesOrMisdemeanorResponses",
            "meet_provider",
            "opportunities"
            # the below are fields only for admin level
            # "is_active",
            # "is_verified",
        ]

class StudentProfileWithUserSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    assigned_library = LibrarySerializer()
    careers_of_interest = CareerSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    mentoring_languages = LanguageSerializer(many=True)
    favorite_genres = GenreSerializer(many=True)

    class Meta:
        model = StudentProfile
        fields = [
            "user",
            "assigned_library",
            "careers_of_interest",
            "mentoring_languages",
            "subjects",
            "favorite_genres",
            "family_status",
            "family_support_level",
            "graduation_obstacle",
            "grade_level",
            "bio",
            "is_onboarded",
            "is_active",
            "approval_status"
            # the below are fields only for admin level
            # "is_active",
            # "is_verified",
        ]
