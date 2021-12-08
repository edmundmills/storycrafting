from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    ordering = ('email',)

    fieldsets = (
        (None, {
            "fields": (
                ('email', 'first_name', 'last_name', 'is_staff',)
                
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', ),
        }),
    )



admin.site.register(User, CustomUserAdmin)