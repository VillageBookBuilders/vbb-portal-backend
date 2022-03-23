from rest_framework import serializers

from vbb.careers.models import Career


class CareerSerializer(serializers.ModelSerializer):
    """
    Career Serializer
    """

    class Meta:
        model = Career
        fields = [
            "id",
            "name",
            "description",
        ]
