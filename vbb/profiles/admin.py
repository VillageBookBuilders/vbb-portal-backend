from django.contrib import admin
from .models import AdvisorProfile, MentorProfile, LibrarianProfile, StudentProfile, Opportunity

# Register your models here.
admin.site.register(Opportunity)
admin.site.register(AdvisorProfile)
admin.site.register(LibrarianProfile)

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):

    list_display = ["get_name", "assigned_library", "get_verified", "approval_status"]
    search_fields = ["user__first_name", "user__last_name", "user__username"]
    list_filter = ("approval_status", "organization", "assigned_library", "user__is_email_verified")

    @admin.display(ordering='user__name', description='name')
    def get_name(self, obj):
        try: 
            return (obj.user.first_name + " " +obj.user.last_name)
        except:
            return "----"

    @admin.display(ordering='user__is_email_verified', description='Email Verified')
    def get_verified(self, obj):
        try: 
            return obj.user.is_email_verified
        except:
            return "----"



@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = ["get_name", "assigned_library", "approval_status"]
    search_fields = ["user__first_name", "user__last_name", "user__username"]
    list_filter = ("approval_status", "assigned_library")

    @admin.display(ordering='user__name', description='name')
    def get_name(self, obj):
        try: 
            return (obj.user.first_name + " " +obj.user.last_name)
        except:
            return "----"

# @admin.register(AdvisorProfile)
# class AdvisorProfileAdmin(admin.ModelAdmin):

#     list_display = ["library", "get_name"]
#     search_fields = ["user__first_name", "user__last_name", "user__username"]
#     list_filter = ("library")

#     @admin.display(ordering='user__name', description='name')
#     def get_name(self, obj):
#         try: 
#             return (obj.user.first_name + " " +obj.user.last_name)
#         except:
#             return "----"



# @admin.register(LibrarianProfile)
# class LibrarianProfileAdmin(admin.ModelAdmin):

#     list_display = ["library", "get_name"]
#     search_fields = ["user__first_name", "user__last_name", "user__username"]
#     list_filter = ("library")


#     @admin.display(ordering='user__name', description='name')
#     def get_name(self, obj):
#         try: 
#             return (obj.user.first_name + " " +obj.user.last_name)
#         except:
#             return "----"
