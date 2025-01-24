from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Education, WorkExperience, Achievement

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_verified')
    list_filter = ('role', 'is_staff', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'role', 'phone')}),
        ('Статус', {'fields': ('is_active', 'is_verified')}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_role', 'rating', 'courses_count', 'reviews_count', 'verification_status']
    list_filter = ['verification_status', 'user__role']
    search_fields = ['user__email', 'bio']
    readonly_fields = ['courses_count', 'reviews_count', 'verified_at']
    
    def get_role(self, obj):
        return obj.user.get_role_display()
    get_role.short_description = 'Роль'

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'degree', 'field_of_study', 'start_date', 'end_date']
    list_filter = ['degree']
    search_fields = ['user__email', 'institution', 'field_of_study']

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'position', 'start_date', 'end_date']
    search_fields = ['user__email', 'company', 'position']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'date']
    search_fields = ['user__email', 'title']
