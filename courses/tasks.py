from celery import shared_task
from django.core.cache import cache
from django.db.models import Avg, Count
from django.utils import timezone
from typing import Dict, Any
import logging

from .models import Course, CourseAnalytics, AnalyticsLog

logger = logging.getLogger(__name__)

@shared_task
def update_course_analytics(course_id: int) -> Dict[str, Any]:
    """
    Обновляет аналитику курса на основе логов
    """
    try:
        course = Course.objects.get(id=course_id)
        analytics, _ = CourseAnalytics.objects.get_or_create(course=course)
        
        # Получаем данные за последние 30 дней
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        logs = AnalyticsLog.objects.filter(
            course=course,
            timestamp__gte=thirty_days_ago
        )
        
        # Агрегируем данные
        stats = logs.aggregate(
            views=Count('id', filter={'event_type': 'view'}),
            completions=Count('id', filter={'event_type': 'complete'}),
            avg_rating=Avg('data__rating', filter={'event_type': 'rate'}),
            total_revenue=Sum('data__amount', filter={'event_type': 'purchase'})
        )
        
        # Обновляем аналитику
        analytics.views_count = stats['views'] or 0
        analytics.completion_rate = (stats['completions'] or 0) / (stats['views'] or 1) * 100
        analytics.average_rating = stats['avg_rating'] or 0
        analytics.revenue = stats['total_revenue'] or 0
        analytics.save()
        
        # Инвалидируем кэш
        cache_key = f'course_analytics:{course_id}'
        cache.delete(cache_key)
        
        return {
            'status': 'success',
            'course_id': course_id,
            'analytics': {
                'views': stats['views'],
                'completions': stats['completions'],
                'avg_rating': stats['avg_rating'],
                'revenue': stats['total_revenue']
            }
        }
        
    except Course.DoesNotExist:
        logger.error(f"Course with id {course_id} not found")
        return {'status': 'error', 'message': 'Course not found'}
    except Exception as e:
        logger.exception(f"Error updating analytics for course {course_id}: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def cleanup_old_analytics_logs(days: int = 90) -> Dict[str, Any]:
    """
    Очищает старые записи аналитики
    """
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        old_logs = AnalyticsLog.objects.filter(timestamp__lt=cutoff_date)
        count = old_logs.count()
        old_logs.delete()
        
        return {
            'status': 'success',
            'deleted_count': count,
            'cutoff_date': cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.exception(f"Error cleaning up old analytics logs: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def recalculate_course_ratings() -> Dict[str, Any]:
    """
    Пересчитывает рейтинги всех курсов
    """
    try:
        courses = Course.objects.all()
        updated_count = 0
        
        for course in courses:
            analytics = CourseAnalytics.objects.filter(course=course).first()
            if not analytics:
                continue
                
            # Получаем все оценки
            ratings = AnalyticsLog.objects.filter(
                course=course,
                event_type='rate'
            ).values_list('data__rating', flat=True)
            
            if ratings:
                # Рассчитываем взвешенный рейтинг
                total_ratings = len(ratings)
                avg_rating = sum(ratings) / total_ratings
                
                # Обновляем аналитику
                analytics.average_rating = avg_rating
                analytics.total_ratings = total_ratings
                analytics.save()
                
                updated_count += 1
                
        return {
            'status': 'success',
            'updated_courses': updated_count
        }
        
    except Exception as e:
        logger.exception(f"Error recalculating course ratings: {str(e)}")
        return {'status': 'error', 'message': str(e)}
