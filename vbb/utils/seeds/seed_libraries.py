import random
from datetime import datetime, timedelta, timezone

from vbb.announcements.models import Announcement
from vbb.libraries.models import Library

library_seeds = [
    {
        "is_accepting_new_mentors": True,
        "library_code": "first_library",
        "name": "First Library Seed",
    },
    {
        "is_accepting_new_mentors": True,
        "library_code": "second_library",
        "name": "Second Library Seed with LONGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg NAME",
    },
    {
        "is_accepting_new_mentors": False,
        "library_code": "third_library",
        "name": "Third Library Seed",
    },
]

announcement_seeds = [
    {
        "text": "We're the first library seed!",
    },
    {
        "text": "We're the second!",
    },
    {
        "text": "We're the third and not accepting new mentors!",
    },
]

random_announcement_seeds = [
    "Random announcement!",
    "Random LONGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg announcement!",
    "Random  THINGS We like to do  announcement!",
]


def seed_libraries() -> None:
    for index, library in enumerate(library_seeds):
        (library, _) = Library.objects.update_or_create(
            library_code=library["library_code"], defaults={**library}
        )
        now = datetime.now(timezone.utc)
        Announcement.objects.create(
            library=library,
            text=announcement_seeds[index]["text"],
            start_date=(now + timedelta(days=10)),
            end_date=(now + timedelta(days=(10 + index))),
        )
        Announcement.objects.create(
            library=library,
            text=random.choice(random_announcement_seeds),
            start_date=(now + timedelta(days=15)),
            end_date=(now + timedelta(days=(10 + index))),
        )
