import pytest
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from courses.tasks import (
    update_course_analytics,
    cleanup_old_analytics_logs,
    recalculate_course_ratings
)
from courses.models import Course, CourseAnalytics, AnalyticsLog

@pytest.mark.django_db
class TestCourseTasks:
    @pytest.fixture
    def course(self):
        return Course.objects.create(
            title='Test Course',
            description='Test Description'
        )
        
    @pytest.fixture
    def analytics_logs(self, course):
        # Создаем тестовые логи
        now = timezone.now()
        
        # Просмотры
        for _ in range(10):
            AnalyticsLog.objects.create(
                course=course,
                event_type='view',
                timestamp=now,
                data={}
            )
            
        # Завершения
        for _ in range(5):
            AnalyticsLog.objects.create(
                course=course,
                event_type='complete',
                timestamp=now,
                data={}
            )
            
        # Оценки
        ratings = [4, 5, 3, 5, 4]
        for rating in ratings:
            AnalyticsLog.objects.create(
                course=course,
                event_type='rate',
                timestamp=now,
                data={'rating': rating}
            )
            
        # Покупки
        amounts = [100, 200, 150]
        for amount in amounts:
            AnalyticsLog.objects.create(
                course=course,
                event_type='purchase',
                timestamp=now,
                data={'amount': amount}
            )
            
    def test_update_course_analytics(self, course, analytics_logs):
        """Тест обновления аналитики курса"""
        result = update_course_analytics(course.id)
        
        assert result['status'] == 'success'
        assert result['course_id'] == course.id
        
        analytics = CourseAnalytics.objects.get(course=course)
        assert analytics.views_count == 10
        assert analytics.completion_rate == 50.0  # 5/10 * 100
        assert analytics.average_rating == 4.2  # (4+5+3+5+4)/5
        assert analytics.revenue == Decimal('450')  # 100+200+150
        
    def test_update_course_analytics_no_course(self):
        """Тест обработки несуществующего курса"""
        result = update_course_analytics(999)
        assert result['status'] == 'error'
        assert 'Course not found' in result['message']
        
    def test_cleanup_old_analytics_logs(self, course, analytics_logs):
        """Тест очистки старых логов"""
        # Создаем старые логи
        old_date = timezone.now() - timedelta(days=100)
        for _ in range(5):
            AnalyticsLog.objects.create(
                course=course,
                event_type='view',
                timestamp=old_date,
                data={}
            )
            
        result = cleanup_old_analytics_logs(days=90)
        
        assert result['status'] == 'success'
        assert result['deleted_count'] == 5
        
    def test_recalculate_course_ratings(self, course, analytics_logs):
        """Тест пересчета рейтингов курсов"""
        result = recalculate_course_ratings()
        
        assert result['status'] == 'success'
        assert result['updated_courses'] == 1
        
        analytics = CourseAnalytics.objects.get(course=course)
        assert analytics.average_rating == 4.2
        assert analytics.total_ratings == 5
