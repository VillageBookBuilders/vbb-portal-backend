from django.contrib import admin
from .models import Library, Computer, LibraryComputerSlots, UserPreferenceSlot, ComputerReservation, Announcement

# Register your models here.
admin.site.register(Library)
admin.site.register(Computer)
admin.site.register(ComputerReservation)
admin.site.register(Announcement)


@admin.register(LibraryComputerSlots)
class LibraryComputerSlotsAdmin(admin.ModelAdmin):

    list_display = ["get_library", "day", "start_time", "end_time", "start_recurring" ,"end_recurring"]
    search_fields = ["library__name"]
    list_filter = ("library__name", "day")

    @admin.display(ordering='library__name', description='library')
    def get_library(self, obj):
        return obj.library.name


@admin.register(UserPreferenceSlot)
class UserPreferenceSlotAdmin(admin.ModelAdmin):

    list_display = ["get_student", "is_recurring"]
    search_fields = ["student__user__first_name", "student__user__last_name"]
    #list_filter = ("day")

    @admin.display(ordering='student__user__first_name', description='student')
    def get_student(self, obj):
        return obj.student.user.first_name
