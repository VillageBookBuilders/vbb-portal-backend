from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from vbb.users.api.views import UserRegisterViewset, UserViewSet, all_users, example_none_protected_route

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("register", UserRegisterViewset)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("does-this-work/", all_users),
    path("no-csrf/", example_none_protected_route),
]
