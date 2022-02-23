from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for VBB.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    time_zone = CharField(max_length=255, default="UTC")

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username
