from django.contrib import admin
from .models import MentorProfile, LibrarianProfile, StudentProfile

# Register your models here.
admin.site.register(MentorProfile)
admin.site.register(LibrarianProfile)
admin.site.register(StudentProfile)
