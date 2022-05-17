import random
from typing import List

from vbb.careers.models import Career
from vbb.language.models import Language
from vbb.subjects.models import Subject
from vbb.users.models import TIMEZONES


def get_time_zone_list(num_of_libs: int) -> List[str]:
    """Returns a list of time zones."""
    time_zones_for_libraries = []
    for _ in range(num_of_libs):
        time_zones_for_libraries.append(random.choice(TIMEZONES)[0])
    return time_zones_for_libraries


def get_language_list(num_of_libs: int) -> List[str]:
    """Returns a list of time zones."""
    languages = Language.objects.all()
    language_for_libraries = []
    for _ in range(num_of_libs):
        language_for_libraries.append(random.choice(languages).id)
    return language_for_libraries


def get_careers_of_interest() -> List[int]:
    num_of_careers = random.choice([2, 3, 4])
    careers = Career.objects.all()
    careers_ids = []
    for _ in range(num_of_careers + 1):
        career = random.choice(careers)
        if career.id not in careers_ids:
            careers_ids.append(career.id)
    return careers_ids


def get_subjects_of_interest() -> List[int]:
    num_of_subjects = random.choice([2, 3, 4])
    subjects = Subject.objects.all()
    subjects_ids = []
    for _ in range(num_of_subjects + 1):
        subject = random.choice(subjects)
        if subject.id not in subjects_ids:
            subjects_ids.append(subject.id)
    return subjects_ids
