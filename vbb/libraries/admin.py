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

    list_display = ["get_library", "day", "start_time", "end_time", "start_recurring" ,"end_recurring"]
    search_fields = ["library__name"]
    list_filter = ("day")

    @admin.display(ordering='library__name', description='Library')
    def get_library(self, obj):
        return obj.library.name
