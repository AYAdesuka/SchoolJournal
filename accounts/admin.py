from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'full_name', 'phone', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'full_name', 'phone', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': ('full_name', 'phone')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {
            'fields': ('full_name', 'phone')
        }),
    )