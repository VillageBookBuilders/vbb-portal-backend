from vbb.language.models import Language
from vbb.organizations.models import Organization
from vbb.profiles.models import MentorProfile
from vbb.users.admin import User
from vbb.utils.seeds.seed_utils import (
    get_careers_of_interest,
    get_language_list,
    get_subjects_of_interest,
    get_time_zone_list,
)

mentor_seeds = [
    {
        "email": "test_mentor1@test.com",
        "has_completed_training": True,
        "interests": "math, reading, farming",
        "name": "Mentor One",
        "phone_number": "123-456-7890",
        "secondary_email": "test_mentor1-secondary@test.com",
    },
    {
        "email": "test_mentor2@test.com",
        "has_completed_training": True,
        "interests": "Religion, animals, math",
        "name": "Mentor Two",
        "phone_number": "123-456-7890",
        "secondary_email": "test_mentor2-secondary@test.com",
    },
    {
        "email": "test_mentor3@test.com",
        "has_completed_training": True,
        "interests": "the night sky, taking care of my brother's and sister's",
        "name": "Mentor Three",
        "phone_number": "123-456-7890",
        "secondary_email": "test_mentor3-secondary@test.com",
    },
    {
        "email": "test_mentor4@test.com",
        "has_completed_training": True,
        "interests": "traveling, mountains, fishing",
        "name": "Mentor test Four",
        "phone_number": "123-456-7890",
        "secondary_email": "test_mentor4-secondary@test.com",
    },
    {
        "email": "test_mentor5@test.com",
        "has_completed_training": True,
        "interests": "space, nursing, english",
        "name": "Five Test Mentor",
        "phone_number": "123-456-7890",
        "secondary_email": "test_mentor5-secondary@test.com",
    },
    {
        "email": "test_mentor6@test.com",
        "has_completed_training": True,
        "interests": "Playing football, dancing, singing",
        "name": "Six Mentor Test",
        "phone_number": "123-456-7890",
        "secondary_email": "test_mentor6-secondary@test.com",
    },
]


def seed_mentors() -> None:
    """Generates Student Seeds with random subject, careers, and time zones"""
    organizations = Organization.objects.all()
    org_count = len(organizations) - 1
    org_index = 0
    time_zone_choices = get_time_zone_list(len(organizations))
    languages = get_language_list(len(organizations))

    for mentor in mentor_seeds:
        org = organizations[org_index]
        assigned_library = org.library
        time_zone = time_zone_choices[org_index]

        careers_of_interest = get_careers_of_interest()
        subjects_of_interest = get_subjects_of_interest()
        (user, _) = User.objects.update_or_create(
            # criteria for the get value
            email=mentor.get("email", ""),
            defaults={
                # values used to update or create
                "name": mentor.get("name", "default name"),
                "time_zone": time_zone,
                "is_mentor": True,
            },
        )
        user.set_password("123")
        user.save()

        (mentor_profile, _) = MentorProfile.objects.update_or_create(
            # criteria for the get value
            user=user,
            defaults={
                # values used to update or create
                "assigned_library": assigned_library,
                "organization": org,
                "application_video_url": "",
                "approval_status": "Approved",
                # has_viewed_donation_page : models.BooleanField(default=False)
                "has_completed_training": mentor["has_completed_training"],
                # has_clicked_facebook_workplace_invite : models.BooleanField(default=False)
                "interests": mentor["interests"],
                "phone_number": mentor["phone_number"],
                "secondary_email": mentor["secondary_email"],
                "is_of_age": True,
            },
        )
        english = Language.objects.filter(english_display_name="English").first()
        english_id = english.id if english else 1
        spanish = Language.objects.filter(english_display_name="Spanish").first()
        spanish_id = spanish.id if spanish else 2

        mentoring_language_ids = [english_id, spanish_id, languages[org_index]]

        mentor_profile.careers.add(*careers_of_interest)
        mentor_profile.mentoring_languages.add(*mentoring_language_ids)
        mentor_profile.subjects.add(*subjects_of_interest)
        mentor_profile.save()

        org_index = org_index + 1 if org_index < org_count else 0
