from vbb.utils.seeds.seed_careers import seed_careers
from vbb.utils.seeds.seed_languages import seed_languages
from vbb.utils.seeds.seed_subjects import seed_subjects


def seed() -> None:
    seed_careers()
    seed_languages()
    seed_subjects()
