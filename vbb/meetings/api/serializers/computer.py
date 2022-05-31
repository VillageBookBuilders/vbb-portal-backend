from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from vbb.meetings.api.serializers.program import ProgramSerializer
from vbb.meetings.models import Computer, Program


class ComputerSerializer(ModelSerializer):

    program = PrimaryKeyRelatedField(queryset=Program.objects.all(), required=True)
    program_object = ProgramSerializer(source="program", read_only=True)

    class Meta:
        model = Computer
        fields = "__all__"
        read_only_fields = ["deleted"]
