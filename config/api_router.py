from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from vbb.careers.views import CareerViewSet
from vbb.language.views import LanguageViewSet
from vbb.libraries.views import LibraryViews
from vbb.meetings.api.viewsets.computer import ComputerViewSet
from vbb.meetings.api.viewsets.program import ProgramViewset
from vbb.meetings.api.viewsets.sessions import SessionViewset
from vbb.meetings.api.viewsets.slot import SlotViewSet
from vbb.profiles.views import (
    MentorConfirmationEmailViewSet,
    MentorProfileViewSet,
    MentorSignUp,
    StudentProfileViewSet,
)
from vbb.subjects.views import SubjectViewSet
from vbb.users.api.views import LoginView, TimezoneViewSet, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("careers", CareerViewSet)  # public
router.register("languages", LanguageViewSet)  # public
router.register("libraries", LibraryViews)
router.register("subjects", SubjectViewSet)  # public
router.register("users", UserViewSet)

# Programs
router.register("programs", ProgramViewset)

# Computers
router.register("computers", ComputerViewSet)

# Slots
router.register("slots", SlotViewSet)

# Sessions
router.register("sessions", SessionViewset)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView().as_view()),  # public
    path(
        "mentor-registration/",
        MentorProfileViewSet().as_view(),
    ),
    path(
        "student-registration/",
        StudentProfileViewSet().as_view(),
    ),
    path("timezones/", TimezoneViewSet().as_view()),  # public
    path("mentor-sign-up/", MentorSignUp().as_view()),  # public
    path(
        "mentor-email-confirmation/", MentorConfirmationEmailViewSet().as_view()
    ),  # public
]
