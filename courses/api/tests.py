import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson, Category, Tag
from accounts.models import TeacherProfile

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_teacher():
    user = User.objects.create_user(
        username='teacher',
        email='teacher@example.com',
        password='teacher123',
        role='teacher'
    )
    return TeacherProfile.objects.create(
        user=user,
        experience_summary='Test experience',
        education_summary='Test education',
        teaching_style='Test style',
        slug='test-teacher'
    )

@pytest.fixture
def test_category():
    return Category.objects.create(
        name='Test Category',
        slug='test-category',
        description='Test description'
    )

@pytest.fixture
def test_tag():
    return Tag.objects.create(
        name='Test Tag',
        slug='test-tag'
    )

@pytest.fixture
def test_course(test_teacher, test_category):
    course = Course.objects.create(
        title='Test Course',
        slug='test-course',
        description='Test description',
        teacher=test_teacher,
        category=test_category,
        max_students=50,
        difficulty_level='beginner',
        language='ru',
        course_type='free',
        status='published'
    )
    return course

@pytest.mark.django_db
class TestCourseAPI:
    def test_list_courses(self, api_client):
        url = reverse('course-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_course_detail(self, api_client, test_course):
        url = reverse('course-detail', kwargs={'slug': test_course.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Course'

    def test_filter_courses_by_category(self, api_client, test_course, test_category):
        url = reverse('course-list')
        response = api_client.get(url, {'category': test_category.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_filter_courses_by_tag(self, api_client, test_course, test_tag):
        test_course.tags.add(test_tag)
        url = reverse('course-list')
        response = api_client.get(url, {'tags': test_tag.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_search_courses(self, api_client, test_course):
        url = reverse('course-list')
        response = api_client.get(url, {'search': 'Test'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

@pytest.mark.django_db
class TestModuleAPI:
    @pytest.fixture
    def test_module(self, test_course):
        return Module.objects.create(
            course=test_course,
            title='Test Module',
            description='Test description'
        )

    def test_list_modules(self, api_client, test_course, test_module):
        url = reverse('module-list', kwargs={'course_slug': test_course.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Требуется авторизация

    def test_list_modules_authorized(self, api_client, test_user, test_course, test_module):
        api_client.force_authenticate(user=test_user)
        url = reverse('module-list', kwargs={'course_slug': test_course.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class TestLessonAPI:
    @pytest.fixture
    def test_module(self, test_course):
        return Module.objects.create(
            course=test_course,
            title='Test Module',
            description='Test description'
        )

    @pytest.fixture
    def test_lesson(self, test_module):
        return Lesson.objects.create(
            module=test_module,
            title='Test Lesson',
            content='Test content'
        )

    def test_list_lessons(self, api_client, test_module, test_lesson):
        url = reverse('lesson-list', kwargs={'module_id': test_module.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Требуется авторизация

    def test_list_lessons_authorized(self, api_client, test_user, test_module, test_lesson):
        api_client.force_authenticate(user=test_user)
        url = reverse('lesson-list', kwargs={'module_id': test_module.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
