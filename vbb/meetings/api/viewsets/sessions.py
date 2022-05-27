from rest_framework.viewsets import ModelViewSet

from vbb.meetings.api.serializers.sessions import SessionSerializer
from vbb.meetings.models import Session


class SlotViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer