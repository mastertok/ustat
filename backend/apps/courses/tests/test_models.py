import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import Course, Category, Module, Lesson, Review

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
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
        order=1
    )

@pytest.mark.django_db
class TestCategoryModel:
    def test_category_creation(self, category):
        assert category.name == 'Programming'
        assert category.description == 'Learn programming'
        assert category.icon == 'code'
        assert str(category) == 'Programming'

@pytest.mark.django_db
class TestCourseModel:
    def test_course_creation(self, course, user, category):
        assert course.title == 'Python Course'
        assert course.instructor == user
        assert course.category == category
        assert course.level == 'beginner'
        assert course.language == 'ru'
        assert str(course) == 'Python Course'

    def test_course_rating_update(self, course, user):
        # Создаем отзывы
        Review.objects.create(course=course, user=user, rating=4, comment='Good')
        Review.objects.create(course=course, user=User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        ), rating=5, comment='Excellent')

        # Проверяем, что средний рейтинг обновился
        course.refresh_from_db()
        assert course.average_rating == 4.5

@pytest.mark.django_db
class TestModuleModel:
    def test_module_creation(self, module, course):
        assert module.title == 'Introduction'
        assert module.course == course
        assert module.order == 1
        assert str(module) == 'Python Course - Introduction'

@pytest.mark.django_db
class TestLessonModel:
    def test_lesson_creation(self, lesson, module):
        assert lesson.title == 'Variables'
        assert lesson.module == module
        assert lesson.duration == '30 minutes'
        assert lesson.order == 1
        assert str(lesson) == 'Python Course - Introduction - Variables'

@pytest.mark.django_db
class TestReviewModel:
    def test_review_creation(self, course, user):
        review = Review.objects.create(
            course=course,
            user=user,
            rating=5,
            comment='Great course!'
        )
        assert review.rating == 5
        assert review.comment == 'Great course!'
        assert str(review) == f'Python Course - testuser - 5★'

    def test_invalid_rating(self, course, user):
        with pytest.raises(ValidationError):
            review = Review(
                course=course,
                user=user,
                rating=6,  # Неверный рейтинг
                comment='Invalid rating'
            )
            review.full_clean()

    def test_duplicate_review(self, course, user):
        Review.objects.create(
            course=course,
            user=user,
            rating=4,
            comment='First review'
        )
        
        # Попытка создать второй отзыв от того же пользователя
        with pytest.raises(Exception):  # Django выбросит IntegrityError
            Review.objects.create(
                course=course,
                user=user,
                rating=5,
                comment='Second review'
            )
