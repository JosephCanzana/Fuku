from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from apps.accounts.models import User


# Custom email filed for user creation
class CustomUserAdmin(UserAdmin, ModelAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email",)}),
    )

admin.site.register(User, CustomUserAdmin)