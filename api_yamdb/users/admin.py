from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('email', 'username',
#                   'role', 'bio', 'first_name', 'last_name',)
#     list_filter = ('email', 'username',
#                   'role', 'first_name', 'last_name',)
#     search_fields = ('email', 'username',)
#     ordering = ('username',)


admin.site.register(CustomUser)
