from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"), {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "mobile_number",
                    "profile_picture",
                    "gender",
                    "is_customer",
                )
            }
        ),
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "first_name", "mobile_number", "is_superuser"]
    search_fields = ["username", 'mobile_number', 'first_name']
