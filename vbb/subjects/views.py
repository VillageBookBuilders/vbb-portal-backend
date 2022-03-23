from rest_framework import viewsets

from vbb.subjects.models import Subject
from vbb.subjects.serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Subject Views from Rest Framework
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
