from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from courses.models import Course, CourseAnalytics

@receiver(post_save, sender=Course)
def create_course_analytics(sender, instance, created, **kwargs):
    """
    Создает объект аналитики при создании курса
    """
    if created:
        CourseAnalytics.objects.create(course=instance)

@receiver([post_save, post_delete], sender=CourseAnalytics)
def invalidate_course_analytics_cache(sender, instance, **kwargs):
    """
    Инвалидирует кэш аналитики при изменении
    """
    cache_key = f'course_analytics:{instance.course.id}'
    cache.delete(cache_key)
