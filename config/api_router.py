from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from vbb.careers.views import CareerViewSet
from vbb.language.views import LanguageViewSet
from vbb.profiles.views import (
    MentorConfirmationEmailViewSet,
    MentorProfileViewSet,
    MentorSignUp,
    StudentProfileViewSet,
)
from vbb.subjects.views import SubjectViewSet
from vbb.users.api.views import (
    TimezoneViewSet,
    UserViewSet,
    example_protected_route,
    login_user,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("languages", LanguageViewSet)
router.register("careers", CareerViewSet)
router.register("subjects", SubjectViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("login/", login_user),
    path("this/", example_protected_route),
    path(
        "mentor-registration/",
        MentorProfileViewSet().as_view(),
    ),
    path(
        "student-registration/",
        StudentProfileViewSet().as_view(),
    ),
    path("timezones/", TimezoneViewSet().as_view()),
    path("mentor-sign-up/", MentorSignUp().as_view()),
    path("mentor-email-confirmation/", MentorConfirmationEmailViewSet().as_view()),
]
