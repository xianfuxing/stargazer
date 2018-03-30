from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


USER_FIELDS = (
    (None, {'fields': ('username', 'email', 'password1', 'password2',)}),
)


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'position', 'is_staff')
    add_fieldsets = USER_FIELDS
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'position', 'department',)}),
    )


admin.site.register(User, UserAdmin)
