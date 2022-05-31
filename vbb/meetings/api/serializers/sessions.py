from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from vbb.meetings.api.serializers.computer import ComputerSerializer
from vbb.meetings.api.serializers.slot import SlotSerializer
from vbb.meetings.models import Computer, Session, Slot


class SessionSerializer(ModelSerializer):

    computer = PrimaryKeyRelatedField(queryset=Computer.objects.all(), required=True)
    computer_object = ComputerSerializer(source="computer", read_only=True)

    slot = PrimaryKeyRelatedField(queryset=Slot.objects.all(), required=True)
    slot_object = SlotSerializer(source="computer", read_only=True)

    class Meta:
        model = Session
        fields = "__all__"
