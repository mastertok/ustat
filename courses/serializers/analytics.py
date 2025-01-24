from rest_framework import serializers
from courses.models import CourseAnalytics, AnalyticsLog
from django.core.validators import MinValueValidator, MaxValueValidator

class CourseAnalyticsSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для аналитики курсов
    """
    class Meta:
        model = CourseAnalytics
        fields = [
            'id',
            'course',
            'views_count',
            'completion_rate',
            'average_rating',
            'revenue'
        ]
        read_only_fields = fields


class CourseAnalyticsDetailSerializer(CourseAnalyticsSerializer):
    """
    Расширенный сериализатор для детальной аналитики курсов
    """
    monthly_views = serializers.IntegerField(read_only=True)
    monthly_rating = serializers.FloatField(read_only=True)
    conversion_rate = serializers.FloatField(read_only=True)
    
    class Meta(CourseAnalyticsSerializer.Meta):
        fields = CourseAnalyticsSerializer.Meta.fields + [
            'monthly_views',
            'monthly_rating',
            'conversion_rate'
        ]


class AnalyticsEventSerializer(serializers.Serializer):
    """
    Сериализатор для событий аналитики
    """
    EVENT_TYPES = (
        ('view', 'Просмотр'),
        ('complete', 'Завершение'),
        ('rate', 'Оценка'),
        ('purchase', 'Покупка'),
    )
    
    event_type = serializers.ChoiceField(choices=EVENT_TYPES)
    timestamp = serializers.DateTimeField(required=False)
    
    # Поля для различных типов событий
    rating = serializers.IntegerField(
        required=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    amount = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    def validate(self, data):
        """
        Проверка наличия необходимых полей для разных типов событий
        """
        event_type = data.get('event_type')
        
        if event_type == 'rate' and 'rating' not in data:
            raise serializers.ValidationError(
                {'rating': 'Поле rating обязательно для события rate'}
            )
            
        if event_type == 'purchase' and 'amount' not in data:
            raise serializers.ValidationError(
                {'amount': 'Поле amount обязательно для события purchase'}
            )
            
        return data


class AnalyticsLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для логов аналитики
    """
    class Meta:
        model = AnalyticsLog
        fields = [
            'id',
            'course',
            'event_type',
            'user',
            'timestamp',
            'data'
        ]
        read_only_fields = fields
