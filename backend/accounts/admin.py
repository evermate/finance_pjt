# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'age', 'is_staff']  # ✅ 'nickname' 제거
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'age'),
        }),
    )
    ordering = ['username']
    search_fields = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)
