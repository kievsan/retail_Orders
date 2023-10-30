from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# admin.site.register(User, UserAdmin)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    user control panel
    """
    model = User
