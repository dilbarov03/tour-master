from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User, Branch, Region


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    list_display = ('id', 'phone', 'full_name', 'phone')
    list_display_links = ('id', 'phone')
    search_fields = ('phone', 'full_name', 'phone')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('phone',)
    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('full_name', 'branch', 'region', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    list_display_links = ('id', 'name')
    list_filter = ('region',)
    search_fields = ('name',)
    list_per_page = 25


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25
