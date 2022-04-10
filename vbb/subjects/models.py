from django.db import models


class Subject(models.Model):
    """
    Subjects of interests for Mentees and Mentors

    Used to help Mentors and Mentees connect on common subject interests
    """

    description = models.TextField(default="")
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
