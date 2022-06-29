from rest_framework import viewsets

from vbb.subjects.models import Subject, Genre
from vbb.subjects.serializers import SubjectSerializer, GenreSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Subject Views from Rest Framework
    """

    authentication_classes = ()
    permission_classes = []
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    Genre Views from Rest Framework
    """

    authentication_classes = ()
    permission_classes = []
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
