from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for VBB.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    password = models.CharField(max_length=255)
    # time_zone is a softly required field. Not required at registration
    # but required to complete registration for all user profiles
    time_zone = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.email


class Organization(models.Model):
    """
    Outside Organization from VBB

    Tipicaly refers to a corporate partner
    """

    email_domain = models.CharField(max_length=255, unique=True)
    is_corporate_org = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    Program site under VBB
    """

    advisors = models.ManyToManyField(User)

    announcements = models.CharField(max_length=255)
    is_accepting_new_mentors = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Languages in VBB's system

    Includes an `english_display_name` as the common connector
    """

    english_display_name = models.CharField(max_length=255, unique=True)
    name_in_naitve_alphabet = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.english_display_name


class Subject(models.Model):
    """
    Subjects of interests for Mentees and Mentors

    Used to help Mentors and Mentees connect on common subject interests
    """

    description = models.TextField(default="")
    name = models.CharField(max_length=255)


class Career(models.Model):
    """
    Career of adult involved with VBB typically Mentors
    """

    description = models.TextField(default="")
    name = models.CharField(max_length=255)


class MentorProfile(models.Model):
    """
    A User's Mentor Profile in VBB

    """

    class MentorApprovalStatus(models.TextChoices):
        APPROVED = "Approved", _("Approved")
        NOT_REVIEWED = "Not Reviewed", _("Not Reviewed")
        REJECTED = "Rejected", _("Rejected")

    assigned_program = models.ForeignKey(
        Program, on_delete=models.DO_NOTHING, null=True
    )
    careers = models.ManyToManyField(Career, related_name="+")
    languages = models.ManyToManyField(Language, related_name="+")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    subjects = models.ManyToManyField(Subject, related_name="+")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Soft requirement for creation but hard requirement for completion or registration
    application_video_url = models.TextField(null=True)
    approval_status = models.CharField(
        max_length=30,
        choices=MentorApprovalStatus.choices,
        default=MentorApprovalStatus.NOT_REVIEWED,
    )
    has_viewed_donation_page = models.BooleanField(default=False)
    has_completed_training = models.BooleanField(default=False)
    has_clicked_facebook_workplace_invite = models.BooleanField(default=False)
    interests = models.TextField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    secondary_email = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Mentor Profile for {self.user.email}"

    @property
    def completed_registration(self) -> bool:
        """
        The completed_registration property.

        Combines both model required fields and soft requirements.
        """
        has_user_timezone = self.get("user").get("time_zone")
        has_application_video = self.get("application_video_url")

        return has_user_timezone and has_application_video
