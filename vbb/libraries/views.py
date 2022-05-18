from typing import Optional

from rest_framework import permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vbb.libraries.models import Library
from vbb.libraries.serializers import LibrarySerializer, LibraryWithComputersSerializer
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication


class LibraryViews(viewsets.ViewSet):
    """All non-admin level Library Views

    Currently only a View Set with a get '/' and detail '/<id>'
    """

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Library.objects.all()

    def list(self, request: Request) -> Response:
        """Returns list of all libraries in the system with limited fields."""
        serialized_libraries = LibrarySerializer(
            self.queryset, context={"request": request}, many=True
        )
        return Response(data=serialized_libraries.data)

    def retrieve(self, request: Request, pk: Optional[int] = None) -> Response:
        """Returns a library detail with slots."""
        try:
            serialized_library = LibraryWithComputersSerializer(
                self.queryset.get(id=pk), context={"request": request}
            )
            return Response(data=serialized_library.data)
        except Library.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AdminLibraryViews(APIView):
    """All Admin level Library Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Returns a list of all Libraries including codes"""
        return Response(data="Not implemented yet")
