from django.db import models
import uuid
from vbb.careers.models import Career
from vbb.language.models import Language
from vbb.libraries.models import Library
from vbb.organizations.models import Organization
from vbb.subjects.models import Subject, Genre
from vbb.users.models import User
from django.utils.translation import gettext_lazy as _

MEET_PROVIDERS =  ((0, 'google'), (1, 'microsoft'), (2, 'zoom'), (3, 'other'), (4, 'none'))

FAMILY_SUPPORT_CHOICES = (
  (1, 'Very supportive'),
  (2, 'Supportive'),
  (3, 'Less supportive'),
  (4, 'Not supportive at all'),
)

GRADE_CHOICES = (
  (1, '1st Grade'),
  (2, '2nd Grade'),
  (3, '3rd Grade'),
  (4, '4th Grade'),
  (5, '5th Grade'),
  (6, '6th Grade'),
  (7, '7th Grade'),
  (8, '8th Grade'),
  (9, '9th Grade'),
  (10, '10th Grade'),
  (11, '11th Grade'),
  (12, '12th Grade'),
)


class Opportunity(models.Model):
    """
    Opportunity that mentor found platform.
    """
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Opportunity"


class MentorProfile(models.Model):
    """
    A User's Mentor Profile in VBB

    """

    class MentorApprovalStatus(models.TextChoices):
        APPROVED = "Approved", ("Approved")
        NOT_REVIEWED = "Not Reviewed", ("Not Reviewed")
        REJECTED = "Rejected", ("Rejected")

    assigned_library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True)
    careers = models.ManyToManyField(Career, related_name="+")
    mentoring_languages = models.ManyToManyField(Language, related_name="+")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="+")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opportunities = models.ManyToManyField(Opportunity, related_name="+")

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
    interests = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    secondary_email = models.CharField(max_length=255, null=True, blank=True)
    is_of_age = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    how_found_us = models.CharField(max_length=1024, null=True, blank=True)
    is_onboarded = models.BooleanField(default=False)
    canMeetConsistently = models.BooleanField(default=False)
    crimesOrMisdemeanor = models.BooleanField(default=False)
    crimesOrMisdemeanorResponses = models.TextField(null=True, blank=True)
    meet_provider = models.IntegerField(choices=MEET_PROVIDERS, null=True, default=0)

    def __str__(self):
        return f"Mentor Profile for {self.user}"

    @property
    def completed_registration(self) -> bool:
        """
        The completed_registration property.

        Combines both model required fields and soft requirements.
        """
        has_user_timezone = bool(self.user.time_zone)
        has_application_video = bool(self.application_video_url) and not bool(
            self.organization
        )
        print("has_user_timezone", has_user_timezone)
        return has_user_timezone and has_application_video


class LibrarianProfile(models.Model):
    """
    Librarian profile for a user
    """

    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Librarian Profile for {self.user}"


class AdvisorProfile(models.Model):
    """
    Librarian profile for a user
    """

    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Advisor Profile for {self.user}"

class StudentProfile(models.Model):
    """
    Student profile for a user
    """

    class StudentApprovalStatus(models.TextChoices):
        APPROVED = "Approved", ("Approved")
        NOT_REVIEWED = "Not Reviewed", ("Not Reviewed")
        REJECTED = "Rejected", ("Rejected")


    assigned_library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)
    careers_of_interest = models.ManyToManyField(Career, related_name="+")
    mentoring_languages = models.ManyToManyField(Language, related_name="+")
    favorite_genres = models.ManyToManyField(Genre, related_name="+")
    subjects = models.ManyToManyField(Subject, related_name="+")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)


    approval_status = models.CharField(
        max_length=50,
        choices=StudentApprovalStatus.choices,
        default=StudentApprovalStatus.NOT_REVIEWED,
    )

    family_status = models.CharField(_("Family Status"), blank=True, max_length=255)
    family_support_level =  models.IntegerField(choices=FAMILY_SUPPORT_CHOICES, null=True, default=0)

    graduation_obstacle = models.CharField(_("Government Obstacle"), blank=True, max_length=255)
    grade_level = models.IntegerField(choices=GRADE_CHOICES, null=True, default=0)

    is_active = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Student profile for {self.user}"
