import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from reviews.models import Review, Reply
from courses.models import Course
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
def test_course(test_teacher):
    return Course.objects.create(
        title='Test Course',
        slug='test-course',
        description='Test description',
        teacher=test_teacher,
        max_students=50,
        difficulty_level='beginner',
        language='ru',
        course_type='free',
        status='published'
    )

@pytest.fixture
def test_review(test_course, test_user):
    return Review.objects.create(
        course=test_course,
        user=test_user,
        rating=5,
        comment='Test review'
    )

@pytest.mark.django_db
class TestReviewAPI:
    def test_list_reviews(self, api_client, test_course, test_review):
        url = reverse('review-list', kwargs={'course_slug': test_course.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_review_unauthorized(self, api_client, test_course):
        url = reverse('review-list', kwargs={'course_slug': test_course.slug})
        data = {
            'rating': 5,
            'comment': 'New review'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_review_authorized(self, api_client, test_user, test_course):
        api_client.force_authenticate(user=test_user)
        url = reverse('review-list', kwargs={'course_slug': test_course.slug})
        data = {
            'rating': 5,
            'comment': 'New review'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['username'] == test_user.username

@pytest.mark.django_db
class TestReplyAPI:
    @pytest.fixture
    def test_reply(self, test_review, test_user):
        return Reply.objects.create(
            review=test_review,
            user=test_user,
            content='Test reply'
        )

    def test_list_replies(self, api_client, test_review, test_reply):
        url = reverse('reply-list', kwargs={'review_id': test_review.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_reply_unauthorized(self, api_client, test_review):
        url = reverse('reply-list', kwargs={'review_id': test_review.id})
        data = {
            'content': 'New reply'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_reply_authorized(self, api_client, test_user, test_review):
        api_client.force_authenticate(user=test_user)
        url = reverse('reply-list', kwargs={'review_id': test_review.id})
        data = {
            'content': 'New reply'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['username'] == test_user.username
