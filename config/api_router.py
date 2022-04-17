from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from vbb.careers.views import CareerViewSet
from vbb.language.views import LanguageViewSet
from vbb.meetings.api.viewsets.computer import ComputerViewSet
from vbb.meetings.api.viewsets.program import ProgramViewset
from vbb.profiles.views import MentorProfileViewSet
from vbb.subjects.views import SubjectViewSet
from vbb.users.api.views import UserViewSet, login_user

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("languages", LanguageViewSet)
router.register("careers", CareerViewSet)
router.register("subjects", SubjectViewSet)

# Programs
router.register("programs", ProgramViewset)

# Computers
router.register("computers", ComputerViewSet)

# Slots

# Sessions

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("login/", login_user),
    path(
        "mentor-registration/",
        MentorProfileViewSet().as_view(),
    ),
]
