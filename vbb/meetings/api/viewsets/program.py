from rest_framework.viewsets import ModelViewSet

from meetings.models import Program
from vbb.meetings.api.serializers.program import ProgramSerializer


class ProgramViewset(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
