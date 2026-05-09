from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'full_name', 'role', 'email', 'phone', 'is_active']
    list_filter   = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering      = ['-date_joined']
    fieldsets     = UserAdmin.fieldsets + (
        ('Informations Clinique', {'fields': ('role', 'phone', 'photo', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Clinique', {'fields': ('role', 'phone')}),
    )