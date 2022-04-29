from vbb.utils.seeds.seed_careers import seed_careers
from vbb.utils.seeds.seed_languages import seed_languages
from vbb.utils.seeds.seed_libraries import seed_libraries
from vbb.utils.seeds.seed_organizations import seed_organizations
from vbb.utils.seeds.seed_subjects import seed_subjects


def seed() -> None:
    seed_careers()
    seed_languages()
    seed_subjects()
    seed_libraries()
    # seed_organizations has to be run after libraries
    seed_organizations()
