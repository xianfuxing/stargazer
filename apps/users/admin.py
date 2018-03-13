from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


USER_FIELDS = (
    (None, {'fields': ('username', 'email', 'password1', 'password2',)}),
)


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'position', 'is_staff')
    add_fieldsets = USER_FIELDS


admin.site.register(User, UserAdmin)