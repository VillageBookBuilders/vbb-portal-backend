from vbb.language.models import Language
from vbb.libraries.models import Library
from vbb.profiles.models import StudentProfile
from vbb.users.admin import User
from vbb.utils.seeds.seed_utils import (
    get_careers_of_interest,
    get_language_list,
    get_subjects_of_interest,
    get_time_zone_list,
)

student_seeds = [
    {
        "interests": "math, reading, farming",
        "name": "Student One",
        "username": "test_student1",
    },
    {
        "interests": "space, nursing, english",
        "name": "Student Two",
        "username": "test_student2",
    },
    {
        "interests": "the night sky, taking care of my brother's and sister's",
        "name": "Student Three",
        "username": "test_student3",
    },
    {
        "interests": "Playing football, dancing, singing",
        "name": "Student test Four",
        "username": "test_student4",
    },
    {
        "interests": "Religion, animals, math",
        "name": "Five Test Student",
        "username": "test_student5",
    },
    {
        "interests": "traveling, mountains, fishing",
        "name": "Six Student Test",
        "username": "test_student6",
    },
]


def seed_students() -> None:
    """Generates Student Seeds with random subject, careers, and time zones"""
    libraries = Library.objects.filter(is_accepting_new_mentors=True)
    lib_count = len(libraries) - 1
    lib_index = 0
    time_zone_choices = get_time_zone_list(len(libraries))
    languages = get_language_list(len(libraries))

    for student in student_seeds:
        assigned_library = libraries[lib_index]
        time_zone = time_zone_choices[lib_index]

        careers_of_interest = get_careers_of_interest()
        subjects_of_interest = get_subjects_of_interest()
        (user, _) = User.objects.update_or_create(
            # criteria for the get value
            username=student.get("username", ""),
            defaults={
                # values used to update or create
                "name": student.get("name", "default name"),
                "time_zone": time_zone,
                "is_student": True,
                "is_mentor": False,
            },
        )
        user.set_password("123")
        user.save()

        (student_profile, _) = StudentProfile.objects.update_or_create(
            user=user,
            defaults={
                "assigned_library": assigned_library,
                "is_verified": True,
            },
        )
        english = Language.objects.filter(english_display_name="English").first()
        english_id = english.id if english else 1
        spanish = Language.objects.filter(english_display_name="Spanish").first()
        spanish_id = spanish.id if spanish else 2

        mentoring_language_ids = [english_id, spanish_id, languages[lib_index]]

        student_profile.careers_of_interest.add(*careers_of_interest)
        student_profile.mentoring_languages.add(*mentoring_language_ids)
        student_profile.subjects.add(*subjects_of_interest)
        student_profile.save()

        lib_index = lib_index + 1 if lib_index < lib_count else 0
