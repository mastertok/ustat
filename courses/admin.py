from django.contrib import admin
from core.models import BaseAdminConfig
from .models import (
    Course, Category, Lesson, Module, 
    Tag, Review, Announcement, Enrollment, CourseUserRole
)

@admin.register(Course)
class CourseAdmin(BaseAdminConfig.get_admin_class(Course)):
    pass

@admin.register(Category)
class CategoryAdmin(BaseAdminConfig.get_admin_class(Category)):
    pass

@admin.register(Module)
class ModuleAdmin(BaseAdminConfig.get_admin_class(Module)):
    pass

@admin.register(Lesson)
class LessonAdmin(BaseAdminConfig.get_admin_class(Lesson)):
    pass

@admin.register(Review)
class ReviewAdmin(BaseAdminConfig.get_admin_class(Review)):
    pass

@admin.register(CourseUserRole)
class CourseUserRoleAdmin(BaseAdminConfig.get_admin_class(CourseUserRole)):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content', 'course__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'progress', 'enrolled_at', 'completed_at')
    list_filter = ('status', 'course', 'enrolled_at')
    search_fields = ('student__username', 'student__email', 'course__title')
    readonly_fields = ('enrolled_at', 'completed_at', 'last_accessed')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('student', 'course', 'status', 'progress')
        }),
        ('Даты', {
            'fields': ('enrolled_at', 'completed_at', 'last_accessed'),
            'classes': ('collapse',)
        })
    )
