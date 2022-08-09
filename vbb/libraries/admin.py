from django.contrib import admin
from .models import Library, Computer, LibraryComputerSlots, UserPreferenceSlot, ComputerReservation, Announcement
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(Library)
admin.site.register(Computer)
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

    # fieldsets = (
    #     (_("Participants"), {"fields": ("student", "mentor", )}),
    #     (
    #         _("Computer Slot"),
    #         {
    #             "fields": ("computer_slot"),
    #         },
    #     ),
    #     (
    #         _("Important Times"),
    #         {
    #             "fields": (
    #                 "start_time", 
    #                 "end_time", 
    #                 "start_recurring", 
    #                 "end_recurring", 
    #                 "is_recurring", 
    #                 ),
    #         },
    #     ),
    # )

    list_display = ["get_library", "get_student", "get_mentor", "is_recurring"]
    search_fields = ["student__first_name", "student__last_name"]
    #list_filter = ("day")

    @admin.display(ordering='student__name', description='student')
    def get_student(self, obj):
        return (obj.student.first_name + " " +obj.student.last_name)
    
    @admin.display(ordering='mentor__name', description='mentor')
    def get_mentor(self, obj):
        return (obj.mentor.first_name + " " +obj.mentor.last_name)

    @admin.display(ordering='library__name', description='library')
    def get_library(self, obj):
        return obj.computer_slot.library.name


@admin.register(ComputerReservation)
class ComputerReservationAdmin(admin.ModelAdmin):

    list_display = ["get_library", "get_student", "get_mentor", "get_computer", "reserve_status", "is_recurring"]
    search_fields = ["student__first_name", "student__last_name", ]
    #list_filter = ("day")

    @admin.display(ordering='student__name', description='student')
    def get_student(self, obj):
        return (obj.student.first_name + " " +obj.student.last_name)
    
    @admin.display(ordering='mentor__name', description='mentor')
    def get_mentor(self, obj):
        return (obj.mentor.first_name + " " +obj.mentor.last_name)

    @admin.display(ordering='library__name', description='library')
    def get_library(self, obj):
        return obj.computer.library.name

    @admin.display(ordering='computer__name', description='computer')
    def get_computer(self, obj):
        return obj.computer.name

