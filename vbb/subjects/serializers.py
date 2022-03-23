from rest_framework import serializers

from vbb.subjects.models import Subject


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
