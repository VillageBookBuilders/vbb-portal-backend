from uuid import uuid4

from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(deleted=False)


class BaseIntModel(models.Model):
    """
    Base Integer Based Model, Integer Based model uses Integers as external and Internal ID's
    """

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True

    def delete(self, *args):
        self.deleted = True
        self.save()


class BaseUUIDModel(BaseIntModel):
    """Base UUID Model uses integers for internal representation and UUID for external Representation"""

    external_id = models.UUIDField(default=uuid4, unique=True, db_index=True)

    class Meta:
        abstract = True
