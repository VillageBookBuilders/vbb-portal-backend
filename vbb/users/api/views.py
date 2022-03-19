from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from vbb.users.api.serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()


class UserRegisterViewset(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = []

    @action(detail=False)
    def verify(self, request):
        if "token" not in request.GET:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


# TODO : Add Authorisation Here
# TODO : Move to Class Based Views
@api_view(["GET"])
def all_users(request: Request) -> Response:
    print(f"protected router {request}")
    serializer = UserSerializer(User.objects.all(), context={"request": request}, many=True)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


# TODO : Add Authorisation Here
# TODO : Move to Class Based Views
@api_view(["GET"])
@permission_classes([])
def example_none_protected_route(request: Request) -> Response:
    print(f"not protected route {request}")
    serializer = UserSerializer(User.objects.all(), context={"request": request}, many=True)
    return Response(status=status.HTTP_200_OK, data=serializer.data)
