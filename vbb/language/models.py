from django.db import models


class Language(models.Model):
    """
    Languages in VBB's system

    Includes an `english_display_name` as the common connector
    """

    english_display_name = models.CharField(max_length=255, unique=True)
    name_in_native_alphabet = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.english_display_name
