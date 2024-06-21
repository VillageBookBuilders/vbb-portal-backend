from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    fieldsets = (
        (None, {"fields": ["password"]}),
        (_("Personal info"), {"fields": ("name", "email", "first_name","last_name", "profileImage", "role","is_student", "is_mentor", "is_librarian", "has_dropped_out")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "drop_out_date")}),
    )
    list_display = ["username", "email", "first_name", "last_name","is_superuser"]
    search_fields = ["first_name", "last_name"]
