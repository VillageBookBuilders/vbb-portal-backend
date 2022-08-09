from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import AdvisorProfile, MentorProfile, LibrarianProfile, StudentProfile, Opportunity

# Register your models here.
admin.site.register(MentorProfile)
admin.site.register(AdvisorProfile)
admin.site.register(LibrarianProfile)
admin.site.register(StudentProfile)
admin.site.register(Opportunity)

@admin.register(MentorProfile)
class MentorProfileAdmin(auth_admin.MentorProfileAdmin):

    # fieldsets = (
    #     (None, {"fields": ["password"]}),
    #     (_("Personal info"), {"fields": ("name", "email", "first_name","last_name", "profileImage", "role","is_student", "is_mentor", "is_librarian")}),
    #     (
    #         _("Permissions"),
    #         {
    #             "fields": (
    #                 "is_active",
    #                 "is_staff",
    #                 "is_superuser",
    #                 "groups",
    #                 "user_permissions",
    #             ),
    #         },
    #     ),
    #     (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    # )
    list_display = ["user.first_name", "user.last_name"]
    search_fields = ["user.first_name", "user.last_name"]