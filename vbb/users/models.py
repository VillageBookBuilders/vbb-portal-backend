import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class User(AbstractUser):
    """
    Default custom user model for VBB.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    # time_zone is a softly required field. Not required at registration
    # but required to complete registration for all user profiles
    time_zone = models.CharField(max_length=255, null=True, choices=TIMEZONES)
    is_librarian = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.email
