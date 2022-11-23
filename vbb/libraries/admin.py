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
    list_filter = ("library", "day")

    @admin.display(ordering='library__name', description='library')
    def get_library(self, obj):
        try:
            return obj.library.name
        except:
            return "----"


@admin.register(UserPreferenceSlot)
class UserPreferenceSlotAdmin(admin.ModelAdmin):


    list_display = ["get_library", "get_student", "get_mentor", "is_recurring"]
    search_fields = ["student__first_name", "student__last_name", "mentor__name"]
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

    list_display = ["get_library", "get_student", "get_mentor", "get_computer", "start_time", "is_recurring"]
    search_fields = ["student__first_name", "student__last_name", "mentor__first_name", "mentor__last_name"]
    list_filter = ("mentor", "student", "start_time")
    actions = ["assign_teams_link_1", "assign_teams_link_2", "assign_teams_link_3", "assign_teams_link_4", "assign_teams_link_5", "assign_teams_link_6", "assign_teams_link_7", "assign_teams_link_8", "assign_teams_link_9"]

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
            return obj.computer.library.name
        except:
            return "----"

    @admin.display(ordering='computer__name', description='computer')
    def get_computer(self, obj):
        try:
            return obj.computer.name
        except:
            return "----"

    @admin.action(description='Cuchapa Computer 1 Teams Link')
    def assign_teams_link_1(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_MjFlZTU4NzctNWJiMS00ZGY2LWFhYTYtMWQ2YzQ0NjU1YTQ2%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="218 197 860 474")

    @admin.action(description='Cuchapa Computer 2 Teams Link')
    def assign_teams_link_2(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZTkzNDEyMjAtODExNi00MmRkLWFlNTMtNmVlMTJkMGFiNGRj%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="270 183 226 493")

    @admin.action(description='Cuchapa Computer 3 Teams Link')
    def assign_teams_link_3(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_Y2Y5ZjI3NDctNjM3NS00ODAwLTk3ZTgtMTFjNTIzMTllZmJl%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="245 522 707 221")

    @admin.action(description='Cuchapa Computer 4 Teams Link')
    def assign_teams_link_4(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_OGNiMGE4ZGEtZjYyNy00ZGJiLTg5YjgtNjViNzcwM2I1ZDY4%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="212 946 235 506")

    @admin.action(description='Cuchapa Computer 5 Teams Link')
    def assign_teams_link_5(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_N2Q4OTc5ODMtZjZlZS00YWI5LWE0YjgtMGM1NDJiMzgzNTJj%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="219 864 488 905")

    @admin.action(description='Adeiso Computer 1 Teams Link')
    def assign_teams_link_6(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_MTc2MmRmOGYtNTkzNy00ODZlLTg0ZDEtYWFlNDc4MTVmYmVm%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="292 615 943 086")

    @admin.action(description='Adeiso Computer 2 Teams Link')
    def assign_teams_link_7(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_OTgyYTA5MTktMjdmYS00M2U1LWI5NWQtNzhhMGYzMjBiMTcz%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="293 791 423 590")

    @admin.action(description='Adeiso Computer 3 Teams Link')
    def assign_teams_link_8(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_OTFlODVjNmQtYzQyZC00Y2YyLTgxMmYtOTRhZTJkZWViYWU4%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="230 785 394 104")

    @admin.action(description='Adeiso Computer 4 Teams Link')
    def assign_teams_link_9(modeladmin, request, queryset):
        queryset.update(conferenceURL= "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NTE2MmM1ZDgtODcwZi00NzNlLWE0OGEtOWU0OTk2NDFhZWJl%40thread.v2/0?context=%7b%22Tid%22%3a%22fd18d236-3ef5-4b90-b883-bfb2882f123b%22%2c%22Oid%22%3a%226cdefbef-fe59-4aa6-ae28-1f351a00206f%22%7d", meetingID="233 754 094 000")
