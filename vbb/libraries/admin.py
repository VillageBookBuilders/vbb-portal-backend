from django.contrib import admin
from .models import Library, Computer, LibraryComputerSlots, UserPreferenceSlot, ComputerReservation, Announcement

# Register your models here.
admin.site.register(Library)
admin.site.register(Computer)
admin.site.register(UserPreferenceSlot)
admin.site.register(ComputerReservation)
admin.site.register(Announcement)


@admin.register(LibraryComputerSlots)
class LibraryComputerSlotsAdmin(admin.ModelAdmin):

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
    list_display = ["get_library", "day", "start_time", "end_time", ]
    search_fields = ["library__name"]

    @admin.display(ordering='library__name', description='Library')
    def get_library(self, obj):
        return obj.library.name
