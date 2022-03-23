from django.db import models

from vbb.careers.models import Career
from vbb.language.models import Language
from vbb.libraries.models import Library
from vbb.organizations.models import Organization
from vbb.subjects.models import Subject
from vbb.users.models import User


class MentorProfile(models.Model):
    """
    A User's Mentor Profile in VBB

    """

    class MentorApprovalStatus(models.TextChoices):
        APPROVED = "Approved", ("Approved")
        NOT_REVIEWED = "Not Reviewed", ("Not Reviewed")
        REJECTED = "Rejected", ("Rejected")

    assigned_library = models.OneToOneField(
        Library, on_delete=models.DO_NOTHING, null=True
    )
    careers = models.ManyToManyField(Career, related_name="+")
    mentoring_languages = models.ManyToManyField(Language, related_name="+")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    subjects = models.ManyToManyField(Subject, related_name="+")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
        has_user_timezone = self.user.time_zone
        has_application_video = self.application_video_url and not self.organization

        return has_user_timezone and has_application_video


class LibrarianProfile(models.Model):
    """
    Librarian profile for a user
    """

    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Librarian Profile for {self.user.email}"
