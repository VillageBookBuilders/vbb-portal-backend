from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
def all_users(request: Request) -> Response:
    print(f"protected router {request}")
    serializer = UserSerializer(
        User.objects.all(), context={"request": request}, many=True
    )
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
@permission_classes([])
def example_none_protected_route(request: Request) -> Response:
    print(f"not protected route {request}")
    serializer = UserSerializer(
        User.objects.all(), context={"request": request}, many=True
    )
    return Response(status=status.HTTP_200_OK, data=serializer.data)
