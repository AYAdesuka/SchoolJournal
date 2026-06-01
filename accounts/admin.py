from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'last_name', 'first_name', 'role', 'phone', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'phone', 'email', 'last_name', 'first_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Дополнительная информация', {'fields': ('role', 'middle_name', 'birth_date', 'phone', 'address')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'role',
                       'last_name', 'first_name', 'middle_name', 'phone'),
        }),
    )