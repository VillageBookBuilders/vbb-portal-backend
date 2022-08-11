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


    list_display = ["get_library", "get_student", "get_mentor", "is_recurring"]
    search_fields = ["student__first_name", "student__last_name"]
    list_filter = ("mentor", "student")

    @admin.display(ordering='student__name', description='student')
    def get_student(self, obj):
        try:
            return (obj.student.first_name + " " +obj.student.last_name)
        except:
            return "----"
    
    @admin.display(ordering='mentor__name', description='mentor')
    def get_mentor(self, obj):
        try:
            return (obj.mentor.first_name + " " +obj.mentor.last_name)
        except:
            return "----"

    @admin.display(ordering='library__name', description='library')
    def get_library(self, obj):
        try:
            return obj.computer_slot.library.name
        except:
            return "----"


@admin.register(ComputerReservation)
class ComputerReservationAdmin(admin.ModelAdmin):

    list_display = ["get_library", "get_student", "get_mentor", "get_computer", "reserve_status", "is_recurring"]
    search_fields = ["student__first_name", "student__last_name", "mentor__first_name", "mentor__last_name"]
    list_filter = ("mentor", "student", "start_time", "reserved_slot")
    actions = ["assign_teams_link"]

    @admin.display(ordering='student__name', description='student')
    def get_student(self, obj):
        return (obj.student.first_name + " " +obj.student.last_name)
    
    @admin.display(ordering='mentor__name', description='mentor')
    def get_mentor(self, obj):
        return (obj.mentor.first_name + " " +obj.mentor.last_name)

    @admin.display(ordering='library__name', description='library')
    def get_library(self, obj):
        try:
            return obj.computer.library.name
        except:
            return "----"

    @admin.display(ordering='computer__name', description='computer')
    def get_computer(self, obj):
        try:
            return obj.computer.name
        except:
            return "----"
    
    @admin.action(description='Assign MS Teams link')
    def assign_teams_link(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_YzY3NjVhN2QtYjY3NC00ZmIwLWEzNWMtOGI3Y2M0OGIyOWUy%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="270 525 555 202")

