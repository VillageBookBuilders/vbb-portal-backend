from django.db import models


class Library(models.Model):
    """
    Library site under VBB
    """

    announcements = models.CharField(max_length=255)
    is_accepting_new_mentors = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
