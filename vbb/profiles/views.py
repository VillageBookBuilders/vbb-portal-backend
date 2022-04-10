from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication
from rest_framework.authentication import BasicAuthentication


class MentorProfileViewSet(APIView):
    """
    Mentor Profile Views from Rest Framework
    """

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Register Mentor form
        """
        user = request.user
        return Response(status=status.HTTP_201_CREATED)
