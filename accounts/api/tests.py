import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from accounts.models import TeacherProfile, ProducerProfile, Specialization

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        role='student'
    )

@pytest.fixture
def test_teacher():
    user = User.objects.create_user(
        username='teacher',
        email='teacher@example.com',
        password='teacher123',
        role='teacher'
    )
    profile = TeacherProfile.objects.create(
        user=user,
        experience_summary='Test experience',
        education_summary='Test education',
        teaching_style='Test style',
        slug='test-teacher'
    )
    return profile

@pytest.fixture
def test_producer():
    user = User.objects.create_user(
        username='producer',
        email='producer@example.com',
        password='producer123',
        role='producer'
    )
    profile = ProducerProfile.objects.create(
        user=user,
        company='Test Company',
        portfolio='http://example.com'
    )
    return profile

@pytest.fixture
def test_specialization():
    return Specialization.objects.create(
        name='Test Specialization',
        slug='test-spec',
        description='Test description'
    )

@pytest.mark.django_db
class TestUserAPI:
    def test_list_users_unauthorized(self, api_client):
        url = reverse('user-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_users_authorized(self, api_client, test_user):
        url = reverse('user-list')
        api_client.force_authenticate(user=test_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN  # Only admin can list users

@pytest.mark.django_db
class TestTeacherProfileAPI:
    def test_list_teachers(self, api_client):
        url = reverse('teacherprofile-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_teacher_detail(self, api_client, test_teacher):
        url = reverse('teacherprofile-detail', kwargs={'pk': test_teacher.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['username'] == 'teacher'

    def test_filter_teachers_by_specialization(self, api_client, test_teacher, test_specialization):
        test_teacher.specializations.add(test_specialization)
        url = reverse('teacherprofile-list')
        response = api_client.get(url, {'specialization': test_specialization.slug})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class TestProducerProfileAPI:
    def test_list_producers(self, api_client):
        url = reverse('producerprofile-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_producer_detail(self, api_client, test_producer):
        url = reverse('producerprofile-detail', kwargs={'pk': test_producer.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['username'] == 'producer'

@pytest.mark.django_db
class TestSpecializationAPI:
    def test_list_specializations(self, api_client):
        url = reverse('specialization-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_specialization_unauthorized(self, api_client):
        url = reverse('specialization-list')
        data = {
            'name': 'New Specialization',
            'slug': 'new-spec',
            'description': 'New description'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
