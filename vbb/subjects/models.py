from django.db import models
import uuid


class Subject(models.Model):
    """
    Subjects of interests for Mentees and Mentors

    Used to help Mentors and Mentees connect on common subject interests
    """
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    description = models.TextField(default="")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subjects"


class Genre(models.Model):
    """
    Genre of books that mentees enjoy.
    """
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    description = models.TextField(default="")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
