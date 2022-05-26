from django.db import models


class Library(models.Model):
    """
    Library site under VBB
    """

    is_accepting_new_mentors = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    library_code = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.name
