from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Department

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields':
                                ('first_name',
                                    'last_name',
                                    'avatar',
                                    'job_position',
                                    'is_researcher',
                                    'acad_position',
                                    'department',
                                    'expertise',
                                    )
                                }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                            'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'acad_position', 'first_name', 'last_name', 'department', 'job_position', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    model = Department