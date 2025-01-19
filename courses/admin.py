from django.contrib import admin
from .models import (
    Course, Category, Lesson, Module, 
    Tag, Review, Announcement, Enrollment
)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'teacher', 'course_type',
        'price', 'status', 'average_rating', 'sales_count'
    )
    list_filter = (
        'status', 'course_type', 'category',
        'difficulty_level', 'language', 'teacher'
    )
    search_fields = ('title', 'description', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('average_rating', 'reviews_count', 'sales_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title', 'slug', 'description', 'excerpt',
                'category', 'tags', 'teacher', 'producer'
            )
        }),
        ('Медиа', {
            'fields': ('cover_image', 'video_intro'),
            'description': 'Загрузите обложку курса и добавьте вводное видео'
        }),
        ('Настройки курса', {
            'fields': (
                'difficulty_level', 'language', 'duration_minutes',
                'max_students', 'enable_qa', 'enable_announcements',
                'enable_reviews'
            ),
            'classes': ('collapse',)
        }),
        ('Цена и тип', {
            'fields': ('course_type', 'price', 'currency', 'discount_price'),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('sales_count', 'average_rating', 'reviews_count'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('status', 'published_at')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'description', 'course__title')
    ordering = ('course', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'content_type', 'order', 'duration_minutes')
    list_filter = ('content_type', 'module__course')
    search_fields = ('title', 'content', 'module__title', 'module__course__title')
    ordering = ('module', 'order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'course', 'created_at')
    search_fields = ('text', 'user__username', 'course__title')
    readonly_fields = ('created_at', 'updated_at')

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
