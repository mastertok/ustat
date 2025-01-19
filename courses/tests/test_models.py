import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from courses.models import (
    Category, Tag, Course, Module, Lesson, Review,
    Announcement, Enrollment, Promocode, Promotion,
    CourseAnalytics, TrafficSource, EmailCampaign
)
from accounts.models import User, TeacherProfile, ProducerProfile

@pytest.fixture
def user1():
    return User.objects.create_user(
        username='testuser1',
        email='test1@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User1',
        role='teacher'
    )

@pytest.fixture
def user2():
    return User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User2',
        role='teacher'
    )

@pytest.fixture
def teacher_profile1(user1):
    return TeacherProfile.objects.create(
        user=user1,
        slug='test-teacher1',
        experience_summary='Test experience 1'
    )

@pytest.fixture
def teacher_profile2(user2):
    return TeacherProfile.objects.create(
        user=user2,
        slug='test-teacher2',
        experience_summary='Test experience 2'
    )

@pytest.fixture
def category():
    return Category.objects.create(
        name='Test Category',
        slug='test-category-1',
        description='Test description'
    )

@pytest.fixture
def tag():
    return Tag.objects.create(
        name='Test Tag',
        slug='test-tag-1'
    )

@pytest.fixture
def course(category, teacher_profile1):
    return Course.objects.create(
        title='Test Course',
        slug='test-course-1',
        description='Test description',
        excerpt='Test excerpt',
        category=category,
        teacher=teacher_profile1,
        difficulty_level='beginner',
        language='ru',
        price=1000,
        currency='KGS',
        status='draft'
    )

@pytest.mark.django_db
class TestCategory:
    def test_create_category(self, category):
        assert category.name == 'Test Category'
        assert category.slug == 'test-category-1'
        assert str(category) == 'Test Category'

    def test_create_subcategory(self, category):
        subcategory = Category.objects.create(
            name='Test Subcategory',
            slug='test-subcategory-1',
            parent=category
        )
        assert subcategory.parent == category

@pytest.mark.django_db
class TestTag:
    def test_create_tag(self, tag):
        assert tag.name == 'Test Tag'
        assert tag.slug == 'test-tag-1'
        assert str(tag) == 'Test Tag'

@pytest.mark.django_db
class TestCourse:
    def test_create_course(self, course, category, teacher_profile1):
        assert course.title == 'Test Course'
        assert course.category == category
        assert course.teacher == teacher_profile1
        assert str(course) == 'Test Course'

    def test_course_status_validation(self, course):
        with pytest.raises(ValidationError):
            course.status = 'invalid'
            course.full_clean()

    def test_course_difficulty_validation(self, course):
        with pytest.raises(ValidationError):
            course.difficulty_level = 'invalid'
            course.full_clean()

    def test_course_language_validation(self, course):
        with pytest.raises(ValidationError):
            course.language = 'invalid'
            course.full_clean()

@pytest.mark.django_db
class TestModule:
    def test_create_module(self, course):
        module = Module.objects.create(
            course=course,
            title='Test Module',
            description='Test description',
            order=1
        )
        assert module.title == 'Test Module'
        assert module.course == course
        assert str(module) == 'Test Module'

@pytest.mark.django_db
class TestLesson:
    def test_create_lesson(self, course):
        module = Module.objects.create(
            course=course,
            title='Test Module'
        )
        lesson = Lesson.objects.create(
            module=module,
            title='Test Lesson',
            content_type='text',
            content='Test content',
            order=1
        )
        assert lesson.title == 'Test Lesson'
        assert lesson.module == module
        assert str(lesson) == 'Test Lesson'

    def test_lesson_content_type_validation(self, course):
        module = Module.objects.create(
            course=course,
            title='Test Module'
        )
        with pytest.raises(ValidationError):
            lesson = Lesson.objects.create(
                module=module,
                title='Test Lesson',
                content_type='invalid',
                content='Test content'
            )
            lesson.full_clean()

@pytest.mark.django_db
class TestReview:
    def test_create_review(self, course, user2):
        review = Review.objects.create(
            course=course,
            user=user2,
            rating=5,
            text='Test review'
        )
        assert review.rating == 5
        assert review.course == course
        assert review.user == user2
        assert str(review) == f'Review by {user2.username} for {course.title}'

    def test_review_rating_validation(self, course, user2):
        with pytest.raises(ValidationError):
            review = Review.objects.create(
                course=course,
                user=user2,
                rating=6,
                text='Test review'
            )
            review.full_clean()

@pytest.mark.django_db
class TestPromocode:
    def test_create_promocode(self, course):
        producer = ProducerProfile.objects.create(
            user=course.teacher.user,
            company='Test Company'
        )
        promocode = Promocode.objects.create(
            code='TEST123',
            discount_percent=10,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timezone.timedelta(days=30),
            max_uses=100,
            created_by=producer
        )
        promocode.courses.add(course)
        assert promocode.code == 'TEST123'
        assert promocode.discount_percent == 10
        assert str(promocode) == 'TEST123'

    def test_promocode_validation(self, course):
        producer = ProducerProfile.objects.create(
            user=course.teacher.user,
            company='Test Company'
        )
        with pytest.raises(ValidationError):
            promocode = Promocode.objects.create(
                code='TEST124',
                discount_percent=101,  # Should be <= 100
                valid_from=timezone.now(),
                valid_until=timezone.now() - timezone.timedelta(days=1),  # Invalid date
                max_uses=100,
                created_by=producer
            )
            promocode.full_clean()

@pytest.mark.django_db
class TestEnrollment:
    def test_create_enrollment(self, course, user2):
        enrollment = Enrollment.objects.create(
            student=user2,
            course=course,
            status='active',
            progress=0
        )
        assert enrollment.student == user2
        assert enrollment.course == course
        assert enrollment.status == 'active'
        assert str(enrollment) == f'{user2.username} - {course.title}'

    def test_enrollment_progress_validation(self, course, user2):
        with pytest.raises(ValidationError):
            enrollment = Enrollment.objects.create(
                student=user2,
                course=course,
                status='active',
                progress=101  # Should be <= 100
            )
            enrollment.full_clean()
