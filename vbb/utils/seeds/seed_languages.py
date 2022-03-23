from vbb.language.models import Language
from vbb.utils.languages import languages


def seed_languages() -> None:
    """
    Seed the database with a list of languages.

    From https://github.com/annexare/Countries and has both English name and
    the name of the language in native alphabet.
    Example element of the list
        "aa": {
          "name": "Afar",
          "native": "Afar"
        },

    Returns:
        None
    """
    for language in languages.values():
        Language.objects.update_or_create(
            english_display_name=language["name"],
            name_in_native_alphabet=language["native"],
        )
