from django.contrib import admin

from vbb.organizations.models import Organization

admin.sites.site.register(Organization)
