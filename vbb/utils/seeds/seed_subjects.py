from vbb.subjects.models import Subject

subjects = [
    {
        "name": "Elementary School Math",
        "description": "Study of numbers and relationships to each other",
    },
    {
        "name": "High School Math",
        "description": "Algebra, Geometry, Trigonometry, Pre-Calculus, and/or Calculus.",
    },
    {
        "name": "Sports",
        "description": "Study of athletes, games, and their rules",
    },
    {
        "name": "Reading for Beginners",
        "description": "Reading introductory level books in a given language",
    },
    {
        "name": "Elementary English",
        "description": "Speaking and conversing in introductory English language",
    },
    {
        "name": "Physics",
        "description": "Study of energy and it's interactions",
    },
    {
        "name": "Chemistry",
        "description": "Study of interactions between materials",
    },
    {
        "name": "Computer Skills",
        "description": "Study of how computers do the things they do and/or how to use them effectively",
    },
    {
        "name": "Business",
        "description": "Study of organizations, their creation, and intended outcomes",
    },
    {
        "name": "Earth Science",
        "description": "Study of natural processes on Earth",
    },
    {
        "name": "Biology",
        "description": "Study of animal interaction and systems",
    },
    {
        "name": "ESL",
        "description": "Study of English as an additional language",
    },
]


def seed_subjects() -> None:
    """
    Seed the database with a list of subjects.

    Returns:
        None
    """
    for subject in subjects:
        Subject.objects.update_or_create(
            name=subject["name"], description=subject["description"]
        )
