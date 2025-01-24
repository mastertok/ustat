from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import F, Sum, Avg
from django.core.cache import cache
from core.api.base import CQRSViewSet, cache_response
from core.monitoring import monitor_view, monitor_db_query
from courses.models import Course, CourseAnalytics, AnalyticsLog
from courses.serializers import (
    CourseAnalyticsSerializer,
    AnalyticsEventSerializer,
    CourseAnalyticsDetailSerializer
)
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CourseAnalyticsViewSet(CQRSViewSet):
    """
    ViewSet для работы с аналитикой курсов
    """
    queryset = CourseAnalytics.objects.all()
    serializer_class = CourseAnalyticsSerializer
    query_serializer_class = CourseAnalyticsDetailSerializer
    command_serializer_class = AnalyticsEventSerializer

    @monitor_view
    @cache_response(timeout=300, key_prefix='course_analytics')
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None) -> Response:
        """
        Получение аналитики по конкретному курсу
        """
        try:
            course = self.get_object()
            analytics = self._get_course_analytics(course)
            
            return Response(analytics)
            
        except Course.DoesNotExist:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception(f"Error getting course analytics: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @monitor_view
    @action(detail=True, methods=['post'])
    def update_analytics(self, request, pk=None) -> Response:
        """
        Обновление аналитики курса через события
        """
        try:
            course = self.get_object()
            serializer = AnalyticsEventSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            event_data = serializer.validated_data
            self._process_analytics_event(course, event_data)
            
            # Инвалидируем кэш
            cache_key = f'course_analytics:{course.id}'
            cache.delete(cache_key)
            
            return Response({'status': 'success'})
            
        except Course.DoesNotExist:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception(f"Error updating course analytics: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @monitor_db_query
    def _get_course_analytics(self, course: Course) -> Dict[str, Any]:
        """
        Получение агрегированной аналитики по курсу
        """
        analytics = CourseAnalytics.objects.filter(course=course).first()
        
        if not analytics:
            return {
                'views_count': 0,
                'completion_rate': 0,
                'average_rating': 0,
                'revenue': 0
            }
            
        # Получаем детальную статистику
        logs = AnalyticsLog.objects.filter(
            course=course,
            timestamp__gte=timezone.now() - timezone.timedelta(days=30)
        )
        
        monthly_stats = logs.aggregate(
            total_views=Sum('views_count'),
            avg_rating=Avg('rating')
        )
        
        return {
            'views_count': analytics.views_count,
            'completion_rate': analytics.completion_rate,
            'average_rating': analytics.average_rating,
            'revenue': analytics.revenue,
            'monthly_views': monthly_stats['total_views'] or 0,
            'monthly_rating': monthly_stats['avg_rating'] or 0
        }

    def _process_analytics_event(self, course: Course, event_data: Dict[str, Any]):
        """
        Обработка события аналитики
        """
        analytics, created = CourseAnalytics.objects.get_or_create(course=course)
        event_type = event_data['event_type']
        
        # Создаем запись в логе
        AnalyticsLog.objects.create(
            course=course,
            event_type=event_type,
            user=self.request.user,
            data=event_data
        )
        
        # Обновляем агрегированные данные
        if event_type == 'view':
            analytics.views_count = F('views_count') + 1
        elif event_type == 'complete':
            analytics.completion_count = F('completion_count') + 1
            analytics.completion_rate = (F('completion_count') * 100.0) / F('views_count')
        elif event_type == 'rate':
            analytics.total_ratings = F('total_ratings') + 1
            analytics.rating_sum = F('rating_sum') + event_data['rating']
            analytics.average_rating = F('rating_sum') / F('total_ratings')
        elif event_type == 'purchase':
            analytics.revenue = F('revenue') + event_data['amount']
            
        analytics.save()
