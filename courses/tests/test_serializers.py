import pytest
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User
from courses.models import Course, Category, Module, Lesson, Review, CourseUserRole
from courses.serializers import (
    CourseSerializer,
    CategorySerializer,
    ModuleSerializer,
    LessonSerializer,
    ReviewSerializer,
    CourseUserRoleSerializer
)

class TestCourseSerializer(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123',
            role='teacher'
        )
        
        self.category = Category.objects.create(
            name='Programming',
            slug='programming'
        )
        
        # Создаем тестовое изображение
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # пустой файл для теста
            content_type='image/jpeg'
        )
        
        self.course = Course.objects.create(
            title='Python Course',
            slug='python-course',
            description='Learn Python',
            category=self.category,
            cover_image=self.image,
            price=100,
            language='ru',
            duration=30
        )
        
        # Добавляем преподавателя к курсу
        CourseUserRole.objects.create(
            course=self.course,
            user=self.teacher,
            role='teacher',
            is_primary=True
        )

    def test_course_serialization(self):
        """Тест сериализации курса"""
        serializer = CourseSerializer(self.course)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Python Course')
        self.assertEqual(data['price'], '100.00')
        self.assertEqual(data['language'], 'ru')
        self.assertEqual(data['category_name'], 'Programming')
        
        # Проверяем наличие вложенных данных
        self.assertIn('teachers', data)
        self.assertIn('reviews', data)
        self.assertIn('modules', data)
        self.assertIn('rating_stats', data)

    def test_course_deserialization(self):
        """Тест десериализации курса"""
        data = {
            'title': 'New Course',
            'description': 'Course description',
            'category': self.category.id,
            'price': 200,
            'language': 'en',
            'duration': 60,
            'difficulty': 'beginner'
        }
        
        serializer = CourseSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class TestReviewSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='student@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        self.category = Category.objects.create(
            name='Programming',
            slug='programming'
        )
        
        self.course = Course.objects.create(
            title='Python Course',
            slug='python-course',
            description='Learn Python',
            category=self.category
        )
        
        self.review = Review.objects.create(
            course=self.course,
            user=self.user,
            rating=5,
            text='Great course!'
        )

    def test_review_serialization(self):
        """Тест сериализации отзыва"""
        serializer = ReviewSerializer(self.review)
        data = serializer.data
        
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['text'], 'Great course!')
        self.assertEqual(data['user_name'], 'John Doe')

class TestModuleSerializer(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Programming',
            slug='programming'
        )
        
        self.course = Course.objects.create(
            title='Python Course',
            slug='python-course',
            description='Learn Python',
            category=self.category
        )
        
        self.module = Module.objects.create(
            course=self.course,
            title='Introduction',
            description='Introduction to Python'
        )
        
        self.lesson = Lesson.objects.create(
            module=self.module,
            title='First Steps',
            content_type='text',
            content='Python basics'
        )

    def test_module_serialization(self):
        """Тест сериализации модуля"""
        serializer = ModuleSerializer(self.module)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Introduction')
        self.assertEqual(data['description'], 'Introduction to Python')
        self.assertIn('lessons', data)
        self.assertEqual(len(data['lessons']), 1)
        self.assertEqual(data['lessons'][0]['title'], 'First Steps')
