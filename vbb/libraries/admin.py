from django.contrib import admin

from vbb.libraries.models import Library

# Register your models here.
admin.sites.site.register(Library)
