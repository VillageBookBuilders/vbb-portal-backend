from rest_framework import viewsets

from vbb.language.models import Language
from vbb.language.serializers import LanguageSerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Language Views from Rest Framework
    """

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
