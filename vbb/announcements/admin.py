from django.contrib import admin

from vbb.announcements.models import Announcement

admin.sites.site.register(Announcement)
