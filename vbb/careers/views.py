from rest_framework import viewsets

from vbb.careers.models import Career
from vbb.careers.serializers import CareerSerializer


class CareerViewSet(viewsets.ModelViewSet):
    """
    Career Views from Rest Framework
    """

    authentication_classes = ()
    permission_classes = []
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
