from django.contrib import admin
from .models import AdvisorProfile, MentorProfile, LibrarianProfile, StudentProfile, Opportunity

# Register your models here.
admin.site.register(AdvisorProfile)
admin.site.register(LibrarianProfile)
admin.site.register(StudentProfile)
admin.site.register(Opportunity)

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):

    list_display = ["get_first_name", "approval_status"]
    search_fields = ["user__first_name"]
    list_filter = ("approval_status", "organization", "assigned_library")

    @admin.display(ordering='user__first_name', description='user first name')
    def get_first_name(self, obj):
        return obj.user.first_name

