from vbb.careers.models import Career

careers = [
    {
        "name": "Architecture and Engineering",
        "description": (
            "People creating or building real world and virtual"
            "things ( may include computer engineers, building architects,"
            "electrical engineers, and many others )"
        ),
    },
    {
        "name": "Arts and Entertainment",
        "description": (
            "People engaged in the production of theater, television, or"
            "other forms of performance from live to pre-recorded ( may"
            "include actors, technicians, vocalists, conductors, producers,"
            "and many others )"
        ),
    },
    {
        "name": "Sports",
        "description": (
            "People engaged in the production and playing of"
            "sports ( may include athletes, coaches, medical staff,"
            "and many others )"
        ),
    },
    {
        "name": "Building and Grounds Cleaning and Maintenance",
        "description": (
            "People engaged in keeping buildings functioning and clean for"
            "use ( may include cleaners, electricians, carpenters,"
            "painters, and many other sub groups )"
        ),
    },
    {
        "name": "Business and Financial Operations",
        "description": (
            "People who keep the cost and spending records for"
            "an organization ( may include accountants, controllers,"
            "investors, and many other sub groups )"
        ),
    },
    {
        "name": "Community and Social Services",
        "description": (
            "People working to provide support and to their"
            "community, often referring to people helping others in crisis"
            "or distress"
        ),
    },
    {
        "name": "Construction and Extraction",
        "description": (
            "People involved in building structures or"
            "gathering ore or other resources"
        ),
    },
    {
        "name": "Education, Training, and Library",
        "description": (
            "People involved in passing knowledge to a group of people"
            "( may include teachers, tutors, librarians, and many others )"
        ),
    },
    {
        "name": "Farming, Fishing, and Forestry",
        "description": (
            "People who grow and gather food and maintain the natural environment"
        ),
    },
    {
        "name": "Food Preparation and Serving Related",
        "description": (
            "People who work in food services that are not related to the"
            "growing or gathering of food ( may include cooks, chefs,"
            "dishwashers, waiters, and many others )"
        ),
    },
    {
        "name": "Healthcare Practitioners",
        "description": (
            "People who work in the medical field. ( may include doctors,"
            "nurses, medical technicians, therapists, and many others )"
        ),
    },
    {
        "name": "Installation, Maintenance, and Repair",
        "description": (
            "People who work on or maintain real world systems"
            "( may include plumbers, electricians, carpenters, and many others)"
        ),
    },
    {
        "name": "Legal",
        "description": (
            "A member of the legal profession working with-in or interacting"
            "with the system ( may include judges, lawyers, aids, and many others )"
        ),
    },
    {
        "name": "Life, Physical, and Social Science",
        "description": (
            "People who study the environment and people in a structured"
            "and organized way."
        ),
    },
    {
        "name": "Military and Protective Services",
        "description": (
            "Service to a government or hired employer to protect people"
            "and property."
        ),
    },
    {
        "name": "Office and Administrative Support",
        "description": (
            "Support of people or institutions through management of"
            "support services for an organization."
        ),
    },
    {
        "name": "Personal Care and Service",
        "description": (
            "Support of individual and their health"
            "( mental, physical, and/or spiritual )"
        ),
    },
]


def seed_careers():
    for career in careers:
        Career.objects.update_or_create(
            name=career["name"], description=career["description"]
        )
