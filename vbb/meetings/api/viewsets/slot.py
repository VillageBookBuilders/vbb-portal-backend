from rest_framework.viewsets import ModelViewSet

from vbb.meetings.api.serializers.slot import SlotSerializer
from vbb.meetings.models import Slot


class SlotViewSet(ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
