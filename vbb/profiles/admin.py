from django.contrib import admin
from .models import MentorProfile, LibrarianProfile, StudentProfile, Opportunity

# Register your models here.
admin.site.register(MentorProfile)
admin.site.register(LibrarianProfile)
admin.site.register(StudentProfile)
admin.site.register(Opportunity)
