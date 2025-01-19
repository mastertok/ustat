import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Course, Category, Module, Lesson, Review

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

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

@pytest.mark.django_db
class TestCourseViewSet:
    def test_list_courses(self, api_client, course):
        response = api_client.get('/api/courses/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Python Course'

    def test_retrieve_course(self, api_client, course, module, lesson):
        response = api_client.get(f'/api/courses/{course.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Python Course'
        assert len(response.data['modules']) == 1
        assert response.data['modules'][0]['title'] == 'Introduction'

    def test_popular_courses(self, api_client, course):
        # Создаем еще один курс с большим количеством студентов
        popular_course = Course.objects.create(
            title='Popular Course',
            description='Very popular course',
            price=2000,
            duration='3 months',
            level='intermediate',
            language='ru',
            category=course.category,
            instructor=course.instructor,
            students_count=100
        )

        response = api_client.get('/api/courses/popular/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data[0]['title'] == 'Popular Course'

    def test_toggle_favorite_authenticated(self, api_client, course, user):
        api_client.force_authenticate(user=user)
        response = api_client.post(f'/api/courses/{course.id}/toggle_favorite/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'added to favorites'

        # Проверяем, что курс добавлен в избранное
        course.refresh_from_db()
        assert course.favorites.filter(id=user.id).exists()

        # Повторный запрос должен удалить из избранного
        response = api_client.post(f'/api/courses/{course.id}/toggle_favorite/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'removed from favorites'

    def test_toggle_favorite_unauthenticated(self, api_client, course):
        response = api_client.post(f'/api/courses/{course.id}/toggle_favorite/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_enroll_authenticated(self, api_client, course, user):
        api_client.force_authenticate(user=user)
        response = api_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'enrolled'

        # Проверяем, что пользователь записан на курс
        course.refresh_from_db()
        assert course.students.filter(id=user.id).exists()
        assert course.students_count == 1

        # Повторная попытка записаться должна вернуть ошибку
        response = api_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_enroll_unauthenticated(self, api_client, course):
        response = api_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_review_authenticated(self, api_client, course, user):
        api_client.force_authenticate(user=user)
        
        # Сначала записываем пользователя на курс
        course.students.add(user)
        
        data = {
            'rating': 5,
            'comment': 'Great course!'
        }
        response = api_client.post(f'/api/courses/{course.id}/review/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['rating'] == 5
        assert response.data['comment'] == 'Great course!'

        # Проверяем, что рейтинг курса обновился
        course.refresh_from_db()
        assert course.average_rating == 5.0

        # Повторная попытка оставить отзыв должна вернуть ошибку
        response = api_client.post(f'/api/courses/{course.id}/review/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_review_unenrolled(self, api_client, course, user):
        api_client.force_authenticate(user=user)
        data = {
            'rating': 5,
            'comment': 'Great course!'
        }
        response = api_client.post(f'/api/courses/{course.id}/review/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_review_unauthenticated(self, api_client, course):
        data = {
            'rating': 5,
            'comment': 'Great course!'
        }
        response = api_client.post(f'/api/courses/{course.id}/review/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCategoryViewSet:
    def test_list_categories(self, api_client, category):
        response = api_client.get('/api/categories/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Programming'

    def test_retrieve_category(self, api_client, category):
        response = api_client.get(f'/api/categories/{category.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Programming'
        assert response.data['description'] == 'Learn programming'
