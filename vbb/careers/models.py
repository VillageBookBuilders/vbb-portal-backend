from django.db import models


class Career(models.Model):
    """
    Career of adult involved with VBB typically Mentors
    """

    description = models.TextField(default="")
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
