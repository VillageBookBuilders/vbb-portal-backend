from rest_framework import serializers

from vbb.announcements.serializers import AnnouncementSerializer
from vbb.libraries.models import Library


class LibrarySerializer(serializers.ModelSerializer):
    announcements = serializers.SerializerMethodField()

    def get_announcements(self, library):
        return AnnouncementSerializer(library.announcement_set.all(), many=True).data

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

    announcements = serializers.SerializerMethodField()

    def get_announcements(self, library):
        AnnouncementSerializer(library.announcement_set.all(), many=True)

    class Meta:
        model = Library
        fields = [
            "announcements",
            "id",
            "is_accepting_new_mentors",
            "name",
        ]
