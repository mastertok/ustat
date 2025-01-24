from rest_framework import viewsets, permissions
from courses.models import CourseAnalytics
from .serializers import CourseAnalyticsSerializer
from core.api.base import CachedViewSetMixin

class CourseAnalyticsViewSet(CachedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра аналитики курсов
    """
    queryset = CourseAnalytics.objects.all()
    serializer_class = CourseAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'course__slug'
    
    def get_queryset(self):
        """
        Фильтруем аналитику по правам доступа
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_staff:
            return queryset
            
        # Для преподавателей показываем только их курсы
        if hasattr(user, 'teacher_profile'):
            return queryset.filter(course__teacher=user.teacher_profile)
            
        # Для остальных пользователей показываем только купленные курсы
        return queryset.filter(course__students=user)
