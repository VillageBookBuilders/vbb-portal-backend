from vbb.libraries.models import Library

library_seeds = [
    {
        "announcements": "We're the first library seed!",
        "is_accepting_new_mentors": True,
        "library_code": "first_library",
        "name": "First Library Seed",
    },
    {
        "announcements": "We're the second!",
        "is_accepting_new_mentors": True,
        "library_code": "second_library",
        "name": "Second Library Seed with LONGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg NAME",
    },
    {
        "announcements": "We're the third and not accepting new mentors!",
        "is_accepting_new_mentors": False,
        "library_code": "third_library",
        "name": "Third Library Seed",
    },
]


def seed_libraries() -> None:
    for library in library_seeds:
        Library.objects.update_or_create(
            library_code=library["library_code"], defaults={**library}
        )
