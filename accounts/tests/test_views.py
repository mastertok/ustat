import pytest
from django.urls import reverse
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import Profile, Education, WorkExperience, Achievement
from django.contrib.auth import get_user_model

User = get_user_model()

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
def client():
    return Client()

@pytest.mark.django_db
class TestProfileView:
    def test_profile_view(self, client, profile):
        url = reverse('accounts:profile', kwargs={'slug': profile.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert 'profile' in response.context
        assert response.context['profile'] == profile

    def test_profile_view_with_courses(self, client, profile):
        url = reverse('accounts:profile', kwargs={'slug': profile.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert 'courses' in response.context

@pytest.mark.django_db
class TestProfileEditView:
    def test_profile_edit_view_unauthorized(self, client, profile):
        url = reverse('accounts:profile_edit')
        response = client.get(url)
        assert response.status_code == 302

    def test_profile_edit_view_authorized(self, client, profile):
        client.login(username='testuser', password='testpass123')
        url = reverse('accounts:profile_edit')
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.context['form'].instance, Profile)

    def test_profile_edit_post(self, client, profile):
        client.login(username='testuser', password='testpass123')
        url = reverse('accounts:profile_edit')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone': '+79001234567',
            'bio': 'Updated bio',
            'social_links': '{"vk": "https://vk.com/test"}',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        profile.refresh_from_db()
        assert profile.user.first_name == 'Updated'
        assert profile.user.last_name == 'Name'
        assert profile.user.email == 'updated@example.com'

@pytest.mark.django_db
class TestEducationViews:
    def test_add_education(self, client, profile):
        client.login(username='testuser', password='testpass123')
        url = reverse('accounts:add_education')
        data = {
            'institution': 'Test University',
            'degree': 'Bachelor',
            'field_of_study': 'Computer Science',
            'start_date': '2020-01-01',
            'end_date': '2024-01-01',
            'description': 'Test description'
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert Education.objects.filter(profile=profile).exists()

    def test_delete_education(self, client, profile):
        client.login(username='testuser', password='testpass123')
        education = Education.objects.create(
            profile=profile,
            institution='Test University',
            degree='Bachelor',
            field_of_study='Computer Science',
            start_date='2020-01-01'
        )
        url = reverse('accounts:delete_education', kwargs={'pk': education.pk})
        response = client.post(url)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert not Education.objects.filter(pk=education.pk).exists()

@pytest.mark.django_db
class TestWorkExperienceViews:
    def test_add_work_experience(self, client, profile):
        client.login(username='testuser', password='testpass123')
        url = reverse('accounts:add_work_experience')
        data = {
            'company': 'Test Company',
            'position': 'Developer',
            'start_date': '2020-01-01',
            'end_date': '2024-01-01',
            'description': 'Test description'
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert WorkExperience.objects.filter(profile=profile).exists()

    def test_delete_work_experience(self, client, profile):
        client.login(username='testuser', password='testpass123')
        experience = WorkExperience.objects.create(
            profile=profile,
            company='Test Company',
            position='Developer',
            start_date='2020-01-01'
        )
        url = reverse('accounts:delete_work_experience', kwargs={'pk': experience.pk})
        response = client.post(url)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert not WorkExperience.objects.filter(pk=experience.pk).exists()

@pytest.mark.django_db
class TestAchievementViews:
    def test_add_achievement(self, client, profile):
        client.login(username='testuser', password='testpass123')
        url = reverse('accounts:add_achievement')
        data = {
            'title': 'Test Achievement',
            'issuer': 'Test Issuer',
            'date_received': '2024-01-01',
            'description': 'Test description'
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert Achievement.objects.filter(profile=profile).exists()

    def test_delete_achievement(self, client, profile):
        client.login(username='testuser', password='testpass123')
        achievement = Achievement.objects.create(
            profile=profile,
            title='Test Achievement',
            issuer='Test Issuer',
            date_received='2024-01-01'
        )
        url = reverse('accounts:delete_achievement', kwargs={'pk': achievement.pk})
        response = client.post(url)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert not Achievement.objects.filter(pk=achievement.pk).exists()
