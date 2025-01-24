from rest_framework import serializers
from courses.models import CourseAnalytics

class CourseAnalyticsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для аналитики курсов
    """
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.SlugField(source='course.slug', read_only=True)
    
    class Meta:
        model = CourseAnalytics
        fields = [
            'id', 'course_title', 'course_slug',
            'views_count', 'completion_count', 'completion_rate',
            'total_ratings', 'average_rating', 'revenue',
            'updated_at'
        ]
        read_only_fields = fields
