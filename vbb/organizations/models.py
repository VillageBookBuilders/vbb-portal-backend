from django.db import models

from vbb.libraries.models import Library


class Organization(models.Model):
    """
    Outside Organization from VBB

    Typically refers to a corporate partner
    """

    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)

    corporate_code = models.CharField(max_length=255, unique=True)
    is_corporate_org = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
