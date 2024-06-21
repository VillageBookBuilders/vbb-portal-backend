import pytz
from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

ROLE_CHOICES = (
  (1, 'Student'),
  (2, 'Mentor'),
  (3, 'Advisor'),
  (4, 'Librarian'),
  (5, 'Admin'),
)


class User(AbstractUser):
    """
    Default custom user model for VBB.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # username is redfined because we need to allow for a null value
    # Mentores will not have one. As defined by AbstractUser it doesn't
    # allow for it to be empty and unique
    username = models.CharField(
        _("username"),
        max_length=150,
        null=True,
        blank=True,
        unique=True,
    )
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = models.CharField(_("First Name of User"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name of User"), blank=True, max_length=255)
    profileImage = models.CharField(_("Profile image url of user"), blank=True, max_length=512)
    gender = models.CharField(_("Gender"), blank=True, max_length=255)
    role = models.IntegerField(choices=ROLE_CHOICES, null=True, default=0)
    # time_zone is a softly required field. Not required at registration
    # but required to complete registration for all user profiles
    time_zone = models.CharField(max_length=255, null=True, choices=TIMEZONES)
    is_email_verified = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)
    has_dropped_out = models.BooleanField(default=False)
    drop_out_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.email:
            return self.email
        return self.username

    def save(self, *args, **kwargs):
        if self.has_dropped_out and self.drop_out_date == None:
            self.drop_out_date = datetime.now(timezone.utc)
        super().save(*args, **kwargs)
