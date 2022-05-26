from django.contrib import admin

from vbb.language.models import Language

admin.sites.site.register(Language)
