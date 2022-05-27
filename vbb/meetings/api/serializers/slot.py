from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from vbb.meetings.api.serializers.computer import ComputerSerializer

from vbb.meetings.models import Slot,Computer


class SlotSerializer(ModelSerializer):

    computer = PrimaryKeyRelatedField(queryset=Computer.objects.all(), required=True)
    computer_object = ComputerSerializer(source="computer", read_only=True)

    class Meta:
        model = Slot
        fields = "__all__"
