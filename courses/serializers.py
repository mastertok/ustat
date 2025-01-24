from rest_framework import serializers
from .models import Course, Category, Module, Lesson, Review, CourseUserRole

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'rating', 'text', 'created_at']
        read_only_fields = ['user']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email

class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""
    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'title', 'content_type',
            'content', 'video_url', 'file', 'order',
            'duration_minutes'
        ]

class ModuleSerializer(serializers.ModelSerializer):
    """Сериализатор для модулей"""
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Module
        fields = [
            'id', 'course', 'title', 'description',
            'order', 'lessons', 'lessons_count'
        ]

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description',
            'parent', 'courses_count', 'active_courses_count',
            'total_students', 'average_course_rating'
        ]

class CourseUserRoleSerializer(serializers.ModelSerializer):
    """Сериализатор для ролей пользователей в курсе"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseUserRole
        fields = [
            'id', 'user', 'user_name', 'role',
            'permissions', 'is_primary', 'added_at'
        ]
        read_only_fields = ['added_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    teachers = CourseUserRoleSerializer(
        source='user_roles',
        many=True,
        read_only=True
    )
    reviews = ReviewSerializer(many=True, read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    rating_stats = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'excerpt',
            'category', 'category_name', 'tags', 'cover_image',
            'video_intro', 'price', 'currency', 'discount_price',
            'difficulty', 'language', 'duration', 'status',
            'type', 'created_at', 'published_at', 'students_count',
            'reviews_count', 'average_rating', 'total_lessons',
            'completion_rate', 'teachers', 'reviews', 'modules',
            'rating_stats'
        ]
        read_only_fields = [
            'slug', 'students_count', 'reviews_count',
            'average_rating', 'total_lessons', 'completion_rate'
        ]
    
    def get_rating_stats(self, obj):
        """Получение статистики по рейтингам"""
        stats = {
            'total_ratings': obj.reviews.count(),
            'rating_distribution': {
                '5': obj.reviews.filter(rating=5).count(),
                '4': obj.reviews.filter(rating=4).count(),
                '3': obj.reviews.filter(rating=3).count(),
                '2': obj.reviews.filter(rating=2).count(),
                '1': obj.reviews.filter(rating=1).count(),
            }
        }
        return stats
