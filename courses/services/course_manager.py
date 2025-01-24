from django.db import transaction
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from courses.models import Course, Module, Lesson, CourseUserRole
from courses.services.analytics import CourseAnalyticsService

class CourseManager:
    """Сервис для управления курсами"""
    
    @staticmethod
    @transaction.atomic
    def create_course(data, teacher):
        """Создает новый курс"""
        course = Course.objects.create(
            title=data['title'],
            description=data['description'],
            category_id=data['category_id'],
            price=data.get('price', 0),
            status='draft'
        )
        
        # Добавляем преподавателя
        CourseUserRole.objects.create(
            course=course,
            user=teacher,
            role='teacher',
            is_primary=True
        )
        
        # Добавляем теги
        if 'tags' in data:
            course.tags.add(*data['tags'])
            
        return course

    @staticmethod
    @transaction.atomic
    def update_course(course, data):
        """Обновляет существующий курс"""
        for field, value in data.items():
            if field == 'tags':
                course.tags.set(value)
            elif hasattr(course, field):
                setattr(course, field, value)
        
        course.save()
        CourseAnalyticsService.invalidate_cache(course)
        return course

    @staticmethod
    @transaction.atomic
    def add_module(course, data):
        """Добавляет новый модуль к курсу"""
        position = course.modules.count() + 1
        return Module.objects.create(
            course=course,
            title=data['title'],
            description=data.get('description', ''),
            position=position
        )

    @staticmethod
    @transaction.atomic
    def add_lesson(module, data):
        """Добавляет новый урок к модулю"""
        position = module.lessons.count() + 1
        return Lesson.objects.create(
            module=module,
            title=data['title'],
            content=data['content'],
            position=position,
            duration=data.get('duration', 0)
        )

    @staticmethod
    def get_course_with_details(course_id):
        """Получает курс со всеми связанными данными"""
        return Course.objects.select_related(
            'category'
        ).prefetch_related(
            'tags',
            'modules__lessons',
            'user_roles__user',
            'reviews'
        ).get(id=course_id)

    @staticmethod
    def get_teacher_courses(teacher, status=None):
        """Получает все курсы преподавателя"""
        courses = Course.objects.filter(
            user_roles__user=teacher,
            user_roles__role='teacher'
        ).select_related(
            'category'
        ).prefetch_related(
            'tags'
        )
        
        if status:
            courses = courses.filter(status=status)
            
        return courses.distinct()

    @staticmethod
    @transaction.atomic
    def publish_course(course):
        """Публикует курс"""
        if not course.is_ready_for_publication():
            raise ValueError("Курс не готов к публикации")
            
        course.status = 'published'
        course.published_at = timezone.now()
        course.save()
        
        # Инвалидируем кеш
        CourseAnalyticsService.invalidate_cache(course)
        
        return course

    @staticmethod
    @transaction.atomic
    def archive_course(course):
        """Архивирует курс"""
        course.status = 'archived'
        course.archived_at = timezone.now()
        course.save()
        
        # Инвалидируем кеш
        CourseAnalyticsService.invalidate_cache(course)
        
        return course

    @staticmethod
    def get_related_courses(course, limit=5):
        """Получает похожие курсы"""
        cache_key = f'related_courses_{course.id}'
        related = cache.get(cache_key)
        
        if related is None:
            # Получаем курсы из той же категории с похожими тегами
            related = Course.objects.filter(
                category=course.category,
                status='published'
            ).exclude(
                id=course.id
            ).annotate(
                common_tags=Count('tags', filter=Q(tags__in=course.tags.all()))
            ).order_by('-common_tags', '-average_rating')[:limit]
            
            cache.set(cache_key, list(related), 3600)  # кешируем на 1 час
            
        return related

    @staticmethod
    def get_popular_courses(category=None, limit=10):
        """Получает популярные курсы"""
        cache_key = f'popular_courses_{category.id if category else "all"}'
        popular = cache.get(cache_key)
        
        if popular is None:
            courses = Course.objects.filter(status='published')
            if category:
                courses = courses.filter(category=category)
                
            popular = courses.annotate(
                student_count=Count('enrollments', distinct=True),
                review_count=Count('reviews', distinct=True)
            ).order_by('-student_count', '-average_rating')[:limit]
            
            cache.set(cache_key, list(popular), 3600)  # кешируем на 1 час
            
        return popular
