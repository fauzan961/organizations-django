from django.contrib import admin
from .models import Organization, Role, CustomUser

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_main")
    search_fields = ("name",)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "organization", "role")
    list_filter = ("organization", "role")
    search_fields = ("username", "email")
