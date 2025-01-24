from django.db.models import Avg, Count, Sum, Q
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

class CourseAnalyticsService:
    CACHE_PREFIX = 'course_analytics_'
    CACHE_TIMEOUT = 3600  # 1 час

    @staticmethod
    def get_cache_key(course_id, metric):
        return f"{CourseAnalyticsService.CACHE_PREFIX}{course_id}_{metric}"

    @classmethod
    def calculate_average_rating(cls, course):
        """Вычисляет и кеширует средний рейтинг курса"""
        cache_key = cls.get_cache_key(course.id, 'avg_rating')
        cached_rating = cache.get(cache_key)
        
        if cached_rating is not None:
            return cached_rating
            
        avg_rating = course.reviews.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0.0
        
        cache.set(cache_key, avg_rating, cls.CACHE_TIMEOUT)
        return avg_rating

    @classmethod
    def get_course_statistics(cls, course):
        """Получает полную статистику курса"""
        cache_key = cls.get_cache_key(course.id, 'statistics')
        cached_stats = cache.get(cache_key)
        
        if cached_stats is not None:
            return cached_stats
            
        stats = {
            'total_students': course.enrollments.count(),
            'active_students': course.enrollments.filter(
                status='active'
            ).count(),
            'completion_rate': cls.calculate_completion_rate(course),
            'average_rating': cls.calculate_average_rating(course),
            'total_revenue': cls.calculate_total_revenue(course),
            'last_month_revenue': cls.calculate_period_revenue(
                course, 
                timezone.now() - timedelta(days=30)
            )
        }
        
        cache.set(cache_key, stats, cls.CACHE_TIMEOUT)
        return stats

    @classmethod
    def calculate_completion_rate(cls, course):
        """Вычисляет процент завершения курса"""
        total_enrollments = course.enrollments.count()
        if not total_enrollments:
            return 0
            
        completed = course.enrollments.filter(
            status='completed'
        ).count()
        
        return (completed / total_enrollments) * 100

    @classmethod
    def calculate_total_revenue(cls, course):
        """Вычисляет общий доход от курса"""
        return course.enrollments.filter(
            payment_status='paid'
        ).aggregate(
            total=Sum('payment_amount')
        )['total'] or 0

    @classmethod
    def calculate_period_revenue(cls, course, start_date):
        """Вычисляет доход за определенный период"""
        return course.enrollments.filter(
            payment_status='paid',
            created_at__gte=start_date
        ).aggregate(
            total=Sum('payment_amount')
        )['total'] or 0

    @classmethod
    def get_popular_modules(cls, course, limit=5):
        """Получает самые популярные модули курса"""
        return course.modules.annotate(
            views_count=Count('lesson_views'),
            completion_rate=Avg('lesson_completions__percent')
        ).order_by('-views_count')[:limit]

    @classmethod
    def get_student_progress(cls, course, student):
        """Получает прогресс студента по курсу"""
        enrollment = course.enrollments.filter(student=student).first()
        if not enrollment:
            return None
            
        total_lessons = course.get_total_lessons()
        completed_lessons = enrollment.completed_lessons.count()
        
        return {
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percent': (completed_lessons / total_lessons * 100) if total_lessons else 0,
            'last_activity': enrollment.last_activity,
            'estimated_completion': cls.estimate_completion_date(enrollment)
        }

    @classmethod
    def estimate_completion_date(cls, enrollment):
        """Оценивает предполагаемую дату завершения курса"""
        if not enrollment.last_activity:
            return None
            
        # Вычисляем среднюю скорость прохождения уроков
        completed_lessons = enrollment.completed_lessons.count()
        days_since_start = (timezone.now() - enrollment.created_at).days
        if not days_since_start or not completed_lessons:
            return None
            
        lessons_per_day = completed_lessons / days_since_start
        remaining_lessons = enrollment.course.get_total_lessons() - completed_lessons
        
        if lessons_per_day <= 0:
            return None
            
        days_to_complete = remaining_lessons / lessons_per_day
        return timezone.now() + timedelta(days=days_to_complete)

    @classmethod
    def invalidate_cache(cls, course):
        """Инвалидирует кеш для курса"""
        cache_keys = [
            cls.get_cache_key(course.id, 'avg_rating'),
            cls.get_cache_key(course.id, 'statistics')
        ]
        cache.delete_many(cache_keys)
