from rest_framework import serializers
from courses.models import Course, Module, Lesson, Announcement, Category, Tag
from accounts.api.serializers import TeacherProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    announcements = AnnouncementSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка курсов с меньшим количеством данных"""
    teacher = TeacherProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'excerpt', 'teacher', 'category', 
                 'tags', 'difficulty_level', 'language', 'course_type', 
                 'price', 'currency', 'status', 'published_at')
