import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import Profile, Education, WorkExperience, Achievement, Specialization
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        role='teacher'
    )

@pytest.fixture
def profile(user):
    return Profile.objects.get(user=user)

@pytest.fixture
def specialization(db):
    return Specialization.objects.create(
        name='Test Specialization',
        description='Test Description',
        slug='test-specialization'
    )

@pytest.mark.django_db
class TestProfileAPI:
    def test_list_profiles(self, api_client, profile):
        url = reverse('api:profile-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['user']['username'] == 'testuser'

    def test_retrieve_profile(self, api_client, profile):
        url = reverse('api:profile-detail', kwargs={'pk': profile.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['user']['username'] == 'testuser'

    def test_filter_profiles_by_role(self, api_client, profile):
        url = reverse('api:profile-list')
        response = api_client.get(url, {'role': 'teacher'})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['user']['role'] == 'teacher'

    def test_filter_profiles_by_specialization(self, api_client, profile, specialization):
        profile.specializations.add(specialization)
        url = reverse('api:profile-list')
        response = api_client.get(url, {'specialization': specialization.slug})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['specializations'][0]['slug'] == specialization.slug

@pytest.mark.django_db
class TestEducationAPI:
    def test_list_education(self, api_client, profile, user):
        api_client.force_authenticate(user=user)
        education = Education.objects.create(
            profile=profile,
            institution='Test University',
            degree='Bachelor',
            field_of_study='Computer Science',
            start_date='2020-01-01'
        )
        url = reverse('api:education-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['institution'] == 'Test University'

    def test_create_education(self, api_client, profile, user):
        api_client.force_authenticate(user=user)
        url = reverse('api:education-list')
        data = {
            'institution': 'New University',
            'degree': 'Master',
            'field_of_study': 'Data Science',
            'start_date': '2020-01-01'
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Education.objects.filter(profile=profile, institution='New University').exists()

@pytest.mark.django_db
class TestWorkExperienceAPI:
    def test_list_work_experience(self, api_client, profile, user):
        api_client.force_authenticate(user=user)
        experience = WorkExperience.objects.create(
            profile=profile,
            company='Test Company',
            position='Developer',
            start_date='2020-01-01'
        )
        url = reverse('api:work-experience-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['company'] == 'Test Company'

    def test_create_work_experience(self, api_client, profile, user):
        api_client.force_authenticate(user=user)
        url = reverse('api:work-experience-list')
        data = {
            'company': 'New Company',
            'position': 'Senior Developer',
            'start_date': '2020-01-01'
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert WorkExperience.objects.filter(profile=profile, company='New Company').exists()

@pytest.mark.django_db
class TestAchievementAPI:
    def test_list_achievements(self, api_client, profile, user):
        api_client.force_authenticate(user=user)
        achievement = Achievement.objects.create(
            profile=profile,
            title='Test Achievement',
            issuer='Test Issuer',
            date_received='2024-01-01'
        )
        url = reverse('api:achievement-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Test Achievement'

    def test_create_achievement(self, api_client, profile, user):
        api_client.force_authenticate(user=user)
        url = reverse('api:achievement-list')
        data = {
            'title': 'New Achievement',
            'issuer': 'New Issuer',
            'date_received': '2024-01-01'
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Achievement.objects.filter(profile=profile, title='New Achievement').exists()
