from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Category, Module, Lesson, Review

User = get_user_model()


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'is_free', 'duration', 'order']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lessons', 'lessons_count']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    instructor = InstructorSerializer()
    modules = ModuleSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 
            'meta_title', 'meta_description', 'meta_keywords',
            'image', 'preview_video', 'price', 'level',
            'language', 'duration', 'category', 'instructor',
            'modules', 'reviews', 'is_favorite', 'is_enrolled',
            'average_rating', 'created_at', 'updated_at'
        ]


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    instructor = InstructorSerializer()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'image', 'price',
            'duration', 'level', 'category', 'instructor',
            'students_count', 'average_rating'
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    instructor = InstructorSerializer()
    modules = ModuleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'image', 'preview_video',
            'price', 'duration', 'level', 'language', 'category',
            'instructor', 'modules', 'reviews', 'students_count',
            'average_rating', 'is_favorite', 'is_enrolled'
        ]

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(id=request.user.id).exists()
        return False

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.students.filter(id=request.user.id).exists()
        return False
