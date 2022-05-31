from rest_framework.viewsets import ModelViewSet

from vbb.meetings.api.serializers.program import ProgramSerializer
from vbb.meetings.models import Program


class ProgramViewset(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
