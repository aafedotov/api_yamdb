from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """ Администрирование пользователей и их ролей."""
    list_display = ('username', 'email', 'role')
    list_filter = ('username',)
    search_fields = ('username', 'role')
    ordering = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
