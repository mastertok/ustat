from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    """Фильтры для курсов"""
    
    # Фильтры по цене
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Фильтр по языку
    language = filters.ChoiceFilter(choices=Course.LANGUAGE_CHOICES)
    
    # Фильтры по рейтингу
    rating_min = filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='average_rating', lookup_expr='lte')
    
    # Фильтры по длительности
    duration_min = filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = filters.NumberFilter(field_name='duration', lookup_expr='lte')
    
    # Фильтр по сложности
    difficulty = filters.ChoiceFilter(choices=Course.DIFFICULTY_CHOICES)
    
    # Фильтр по статусу
    status = filters.ChoiceFilter(choices=Course.STATUS_CHOICES)
    
    # Фильтр по категории
    category = filters.NumberFilter(field_name='category__id')
    
    # Поиск по названию и описанию
    search = filters.CharFilter(method='filter_search')
    
    def filter_search(self, queryset, name, value):
        """Поиск по названию и описанию курса"""
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(excerpt__icontains=value)
        )
    
    class Meta:
        model = Course
        fields = [
            'price_min', 'price_max',
            'language',
            'rating_min', 'rating_max',
            'duration_min', 'duration_max',
            'difficulty',
            'status',
            'category',
            'search'
        ]
