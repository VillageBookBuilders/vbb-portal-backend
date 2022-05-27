from rest_framework.serializers import ModelSerializer

from vbb.meetings.models import Slot


class SlotSerializer(ModelSerializer):
    class Meta:
        model = Slot
        fields = "__all__"
