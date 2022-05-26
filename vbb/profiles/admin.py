from django.contrib import admin

from vbb.profiles.models import MentorProfile, StudentProfile

admin.sites.site.register(StudentProfile)
admin.sites.site.register(MentorProfile)
