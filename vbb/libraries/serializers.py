from rest_framework import serializers

from vbb.libraries.models import Library


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = [
            "announcements",
            "is_accepting_new_mentors",
            "name",
        ]
