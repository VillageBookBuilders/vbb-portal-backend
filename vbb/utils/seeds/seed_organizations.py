import random

from vbb.libraries.models import Library
from vbb.organizations.models import Organization

organization_seeds = [
    {
        "corporate_code": "first_org",
        "is_corporate_org": True,
        "name": "First Org",
    },
    {
        "corporate_code": "second_org",
        "is_corporate_org": True,
        "name": "Second Org with Long Nameeeeeeeeeeee",
    },
    {
        "corporate_code": "third_org",
        "is_corporate_org": True,
        "name": "Third Org with Longggggggggggggeeeeeeeeeeerr Nameeeeeeeeeeee",
    },
]


def seed_organizations() -> None:
    libraries = Library.objects.filter(is_accepting_new_mentors=True)
    for org in organization_seeds:
        library = random.choice(libraries)
        (org, _) = Organization.objects.update_or_create(
            corporate_code=org["corporate_code"], defaults={**org}
        )
        org.library = library
        org.save()
