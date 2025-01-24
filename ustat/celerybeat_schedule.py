from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Обновление аналитики каждый час
    'update-course-analytics': {
        'task': 'courses.tasks.update_course_analytics',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    
    # Очистка старых логов каждый день в 3 часа ночи
    'cleanup-old-analytics-logs': {
        'task': 'courses.tasks.cleanup_old_analytics_logs',
        'schedule': crontab(minute=0, hour=3),
        'kwargs': {'days': 90},
    },
    
    # Пересчет рейтингов каждый день в 4 часа ночи
    'recalculate-course-ratings': {
        'task': 'courses.tasks.recalculate_course_ratings',
        'schedule': crontab(minute=0, hour=4),
    },
}
