from typing import Optional

from rest_framework import permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vbb.users.models import User
from vbb.users.serializers import UserSerializer
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication
