from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Profile, Specialization, 
    Education, WorkExperience, Achievement
)

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'role', 'bio', 'avatar', 'phone')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_role', 'rating', 'created_at']
    list_filter = ['user__role']
    search_fields = ['user__username', 'user__email']
    
    def get_role(self, obj):
        return obj.user.get_role_display()
    get_role.short_description = 'Роль'

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['profile', 'institution', 'degree', 'field_of_study', 'start_date', 'end_date']
    list_filter = ['degree', 'institution']
    search_fields = ['institution', 'degree', 'field_of_study']

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['profile', 'company', 'position', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'company']
    search_fields = ['company', 'position', 'description']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title', 'date_received', 'issuer']
    list_filter = ['date_received', 'issuer']
    search_fields = ['title', 'description', 'issuer']

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
