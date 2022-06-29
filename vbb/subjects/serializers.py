from rest_framework import serializers

from vbb.subjects.models import Subject, Genre


class SubjectSerializer(serializers.ModelSerializer):
    """
    Subject Serializer
    """

    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "description",
        ]

class GenreSerializer(serializers.ModelSerializer):
    """
    Genre Serializer
    """

    class Meta:
        model = Genre
        fields = [
            "id",
            "name",
            "description",
        ]
