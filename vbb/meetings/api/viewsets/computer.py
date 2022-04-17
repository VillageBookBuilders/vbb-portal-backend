from rest_framework.viewsets import ModelViewSet

from vbb.meetings.api.serializers.computer import ComputerSerializer
from vbb.meetings.models import Computer


class ComputerViewSet(ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
