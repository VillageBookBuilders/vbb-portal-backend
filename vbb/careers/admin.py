from django.contrib import admin

from vbb.careers.models import Career

admin.sites.site.register(Career)
