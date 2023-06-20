from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

#We wrote the below code so that user's password should not be editable in admin panel
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
