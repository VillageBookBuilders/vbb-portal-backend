from rest_framework import serializers

from vbb.careers.serializers import CareerSerializer
from vbb.language.serializers import LanguageSerializer
from vbb.libraries.serializers import LibrarySerializer
from vbb.profiles.models import MentorProfile, StudentProfile, Opportunity
from vbb.subjects.serializers import SubjectSerializer, GenreSerializer


class OpportunitySerializer(serializers.ModelSerializer):
    """
    Opportunity Serializer
    """

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "name",
        ]


class MentorProfileSerializer(serializers.ModelSerializer):
    assigned_library = LibrarySerializer()
    careers = CareerSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    mentoring_languages = LanguageSerializer(many=True)

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
            # the below are fields only for admin level
            # "is_active",
            # "is_verified",
        ]
