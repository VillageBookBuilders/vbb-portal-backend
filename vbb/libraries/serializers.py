from rest_framework import serializers

from vbb.libraries.models import Library


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = [
            "announcements",
            "id",
            "is_accepting_new_mentors",
            "name",
        ]


class LibraryWithComputersSerializer(serializers.ModelSerializer):
    """Should also include all of the slot and session data"""

    class Meta:
        model = Library
        fields = [
            "announcements",
            "id",
            "is_accepting_new_mentors",
            "name",
        ]
