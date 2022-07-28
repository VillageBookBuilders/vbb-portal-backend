from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from vbb.careers.views import CareerViewSet
from vbb.language.views import LanguageViewSet
from vbb.libraries.views import (LibraryViews, RetrieveLibraryStudentPreferencesViews,
LibraryComputerSlotViews, UserPreferenceSlotViews,
ComputerReservationViews, BookComputerReservationViews,
ComputerViews, RetrieveUserPreferenceSlotViews,LibraryComputerReservationViews,
RetrieveComputerReservationViews, LibraryStudentViews, LibraryMentorViews,
LibraryDetailViews, AnnouncementViews, RetrieveLibraryComputerViews, RetrieveLibraryStudentsViews, RetrieveLibraryMentorsViews)
from vbb.profiles.views import (
    MentorConfirmationEmailViewSet,
    MentorProfileViewSet,
    MentorSignUp,
    StudentProfileViewSet,
    StudentSignUp,
    OpportunityViewSet,
    ApproveStudentViewSet,
    ApproveMentorViewSet
)
from vbb.subjects.views import SubjectViewSet, GenreViewSet
from vbb.users.api.views import (
    LoginView,
    TimezoneViewSet,
    UserViewSet,
    example_protected_route,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("languages", LanguageViewSet)
router.register("careers", CareerViewSet)
router.register("subjects", SubjectViewSet)
router.register("libraries", LibraryViews)
router.register("genres", GenreViewSet)
router.register("opportunity", OpportunityViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView().as_view()),
    path("this/", example_protected_route),
    path("mentor-sign-up/", MentorSignUp().as_view()),
    path(
        "complete-mentor-onboard/",
        MentorProfileViewSet().as_view(),
    ),
    path(
        "profile/mentor/",
        MentorProfileViewSet().as_view(),
    ),
    path(
        "student-sign-up/",
        StudentSignUp().as_view(),
    ),
    path(
        "mentors/status-update/",
        ApproveMentorViewSet().as_view(),
    ),
    path(
        "students/status-update/",
        ApproveStudentViewSet().as_view(),
    ),
    path(
        "complete-student-onboard/",
        StudentProfileViewSet().as_view(),
    ),
    path(
        "library/detail/<str:uniqueID>",
        LibraryDetailViews().as_view(),
    ),
    path(
        "library/all-computers/<str:uniqueID>",
        RetrieveLibraryComputerViews().as_view(),
    ),


    path(
        "library/students/<int:id>",
        LibraryStudentViews().as_view(),
    ),

    path(
        "library/all-students/<str:uniqueID>",
        RetrieveLibraryStudentsViews().as_view(),
    ),

    path(
        "library/mentors/<int:id>",
        LibraryMentorViews().as_view(),
    ),

    path(
        "library/all-mentors/<str:uniqueID>",
        RetrieveLibraryMentorsViews().as_view(),
    ),
    path(
        "library/announcements/",
        AnnouncementViews().as_view(),
    ),
    path(
        "library/announcements/<str:uniqueID>",
        AnnouncementViews().as_view(),
    ),
    path(
        "library/computers/<str:uniqueID>",
        ComputerViews().as_view(),
    ),
    path(
        "library/computers/",
        ComputerViews().as_view(),
    ),
    path(
        "library/computer-reservations/<str:uniqueID>",
        LibraryComputerReservationViews().as_view(),
    ),
    path(
        "library/all-computer-reservations/<str:uniqueID>",
        RetrieveComputerReservationViews().as_view(),
    ),
    path(
        "library/student-slots/<str:uniqueID>",
        RetrieveUserPreferenceSlotViews().as_view(),
    ),
    path(
        "library-slots/",
        LibraryComputerSlotViews().as_view(),
    ),
    path(
        "library-slots/detail/<str:uniqueID>",
        LibraryComputerSlotViews().as_view(),
    ),
    path(
        "library-student-slots/detail/<str:uniqueID>",
        RetrieveLibraryStudentPreferencesViews().as_view(),
    ),
    path(
        "user-preference-slots/",
        UserPreferenceSlotViews().as_view(),
    ),
    path(
        "user-preference-slots/detail/<str:uniqueID>",
        UserPreferenceSlotViews().as_view(),
    ),

    path(
        "computer-reservations/",
        ComputerReservationViews().as_view(),
    ),

    path(
        "book-student-reservations/",
        BookComputerReservationViews().as_view(),
    ),
    path("timezones/", TimezoneViewSet().as_view()),
    path("mentor-email-confirmation/", MentorConfirmationEmailViewSet().as_view()),
]
