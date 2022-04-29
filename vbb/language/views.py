from rest_framework import viewsets

from vbb.language.models import Language
from vbb.language.serializers import LanguageSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    """
    Language Views from Rest Framework
    """

    authentication_classes = ()
    permission_classes = []
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
