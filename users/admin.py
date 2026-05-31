from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'surname', 'is_staff']
    list_filter = ['is_staff', 'is_superuser']
    search_fields = ['email', 'name', 'surname']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('name', 'surname', 'email')}),
    )
