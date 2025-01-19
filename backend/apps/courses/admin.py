from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Category, Module, Lesson, Review

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'price', 'level', 'language', 'created_at']
    list_filter = ['category', 'level', 'language', 'created_at']
    search_fields = ['title', 'description', 'instructor__username', 'instructor__email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title', 'slug', 'description', 'image',
                'preview_video', 'price', 'level', 'language', 'duration',
                'category', 'instructor'
            )
        }),
        ('SEO настройки', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
            'description': format_html('''
                <p><strong>Рекомендации по SEO:</strong></p>
                <ul>
                    <li>Meta заголовок: 50-60 символов</li>
                    <li>Meta описание: 150-160 символов</li>
                    <li>Ключевые слова: 5-10 слов, разделенных запятыми</li>
                </ul>
                <p>Если поля не заполнены, они будут автоматически сгенерированы из основной информации курса.</p>
            ''')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    prepopulated_fields = {'slug': ('title',)}

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 300px"/>',
                obj.image.url
            )
        return 'Нет изображения'
    preview_image.short_description = 'Предпросмотр изображения'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name', 'description']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'description', 'course__title']
    ordering = ['course', 'order']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'is_free', 'duration']
    list_filter = ['module__course', 'is_free']
    search_fields = ['title', 'content', 'module__title']
    ordering = ['module', 'order']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['comment', 'user__username', 'course__title']
    readonly_fields = ['created_at']
