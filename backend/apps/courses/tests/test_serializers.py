import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from ..models import Course, Category, Module, Lesson, Review
from ..serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    CategorySerializer,
    ReviewSerializer
)

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def category():
    return Category.objects.create(
        name='Programming',
        description='Learn programming',
        icon='code'
    )

@pytest.fixture
def course(user, category):
    return Course.objects.create(
        title='Python Course',
        description='Learn Python programming',
        price=1000,
        duration='2 months',
        level='beginner',
        language='ru',
        category=category,
        instructor=user
    )

@pytest.fixture
def module(course):
    return Module.objects.create(
        course=course,
        title='Introduction',
        description='Introduction to Python',
        order=1
    )

@pytest.fixture
def lesson(module):
    return Lesson.objects.create(
        module=module,
        title='Variables',
        description='Learn about variables',
        content='Variables are...',
        duration='30 minutes',
        is_free=True,
        order=1
    )

@pytest.fixture
def review(course, user):
    return Review.objects.create(
        course=course,
        user=user,
        rating=5,
        comment='Great course!'
    )

@pytest.fixture
def request_factory():
    return APIRequestFactory()

@pytest.mark.django_db
class TestCategorySerializer:
    def test_category_serializer(self, category):
        serializer = CategorySerializer(category)
        assert serializer.data['name'] == 'Programming'
        assert serializer.data['description'] == 'Learn programming'
        assert serializer.data['icon'] == 'code'

@pytest.mark.django_db
class TestCourseListSerializer:
    def test_course_list_serializer(self, course, user, request_factory):
        request = request_factory.get('/')
        request.user = user
        context = {'request': request}
        
        serializer = CourseListSerializer(course, context=context)
        data = serializer.data
        
        assert data['title'] == 'Python Course'
        assert data['price'] == '1000.00'
        assert data['level'] == 'beginner'
        assert data['category']['name'] == 'Programming'
        assert data['instructor']['username'] == 'testuser'

@pytest.mark.django_db
class TestCourseDetailSerializer:
    def test_course_detail_serializer(self, course, module, lesson, review, user, request_factory):
        request = request_factory.get('/')
        request.user = user
        context = {'request': request}
        
        serializer = CourseDetailSerializer(course, context=context)
        data = serializer.data
        
        assert data['title'] == 'Python Course'
        assert data['price'] == '1000.00'
        assert data['level'] == 'beginner'
        assert data['language'] == 'ru'
        assert data['category']['name'] == 'Programming'
        assert data['instructor']['username'] == 'testuser'
        assert len(data['modules']) == 1
        assert data['modules'][0]['title'] == 'Introduction'
        assert len(data['modules'][0]['lessons']) == 1
        assert data['modules'][0]['lessons'][0]['title'] == 'Variables'
        assert len(data['reviews']) == 1
        assert data['reviews'][0]['rating'] == 5
        assert data['average_rating'] == 5.0
        assert data['is_enrolled'] is False
        assert data['is_favorite'] is False

@pytest.mark.django_db
class TestReviewSerializer:
    def test_review_serializer_create(self, course, user, request_factory):
        request = request_factory.post('/')
        request.user = user
        context = {'request': request}
        
        data = {
            'rating': 4,
            'comment': 'Good course'
        }
        
        serializer = ReviewSerializer(data=data, context=context)
        assert serializer.is_valid()
        
        review = serializer.save(course=course)
        assert review.rating == 4
        assert review.comment == 'Good course'
        assert review.user == user
        
        # Проверяем, что средний рейтинг курса обновился
        course.refresh_from_db()
        assert course.average_rating == 4.0

    def test_review_serializer_invalid_rating(self, course, user, request_factory):
        request = request_factory.post('/')
        request.user = user
        context = {'request': request}
        
        data = {
            'rating': 6,  # Неверный рейтинг
            'comment': 'Invalid rating'
        }
        
        serializer = ReviewSerializer(data=data, context=context)
        assert not serializer.is_valid()
        assert 'rating' in serializer.errors
