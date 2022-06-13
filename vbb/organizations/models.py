from django.db import models
import uuid

from vbb.libraries.models import Library

MEET_PROVIDERS =  ((0, 'google'), (1, 'microsoft'), (2, 'zoom'), (3, 'other'), (4, 'none'))
ORG_STATUS =  ((0, 'pending'), (1, 'active'), (2, 'rejected'), (3, 'inactive'))

class Organization(models.Model):
    """
    Outside Organization from VBB

    Typically refers to a corporate partner
    """

    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)
    corporate_code = models.CharField(max_length=255, unique=True)
    is_corporate_org = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    default_meet_provider = models.IntegerField(choices=MEET_PROVIDERS, null=True, default=0)
    status = models.IntegerField(choices=ORG_STATUS, null=True, default=0)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    country= models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
