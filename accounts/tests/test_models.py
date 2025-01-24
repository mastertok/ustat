import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from accounts.models import User, Profile

class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='teacher'
        )

    def test_user_creation(self):
        """Проверяем создание пользователя"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'teacher')
        self.assertFalse(self.user.is_verified)
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str(self):
        """Проверяем строковое представление пользователя"""
        self.assertEqual(str(self.user), 'test@example.com')

    def test_user_unique_email(self):
        """Проверяем уникальность email"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',
                password='anotherpass123'
            )

    def test_superuser_creation(self):
        """Проверяем создание суперпользователя"""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

class TestProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='teacher'
        )
        self.profile = Profile.objects.get(user=self.user)  # Profile создается автоматически

    def test_profile_creation(self):
        """Проверяем автоматическое создание профиля"""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.rating, 0)
        self.assertEqual(self.profile.courses_count, 0)
        self.assertEqual(self.profile.reviews_count, 0)

    def test_profile_str(self):
        """Проверяем строковое представление профиля"""
        self.assertEqual(str(self.profile), f'Профиль {self.user}')

    def test_role_specific_data(self):
        """Проверяем работу с данными специфичными для роли"""
        # Тестируем данные учителя
        teacher_data = {
            'expertise': ['Python', 'Django'],
            'experience_years': 5
        }
        self.profile.update_role_data(teacher_data)
        self.assertEqual(
            self.profile.get_role_specific_data(),
            teacher_data
        )

        # Меняем роль на студента и проверяем новые данные
        self.user.role = 'student'
        self.user.save()
        student_data = {
            'level': 'intermediate',
            'completed_courses': [1, 2, 3]
        }
        self.profile.update_role_data(student_data)
        self.assertEqual(
            self.profile.get_role_specific_data(),
            student_data
        )

    def test_rating_validation(self):
        """Проверяем валидацию рейтинга"""
        with self.assertRaises(ValidationError):
            self.profile.rating = -1
            self.profile.full_clean()
        
        with self.assertRaises(ValidationError):
            self.profile.rating = 6
            self.profile.full_clean()

        # Проверяем допустимые значения
        self.profile.rating = 4.5
        self.profile.full_clean()  # Не должно вызывать исключение

class TestProfileCustomUrl(TestCase):
    def setUp(self):
        self.teacher1 = User.objects.create(
            email='teacher1@example.com',
            first_name='John',
            last_name='Doe',
            role='teacher'
        )
        self.teacher2 = User.objects.create(
            email='teacher2@example.com',
            first_name='Jane',
            last_name='Smith',
            role='teacher'
        )
        self.student = User.objects.create(
            email='student@example.com',
            role='student'
        )

    def test_custom_url_generation_from_name(self):
        """Тест генерации URL из имени и фамилии"""
        profile = Profile.objects.create(user=self.teacher1)
        self.assertEqual(profile.custom_url, 'john-doe')

    def test_custom_url_generation_without_name(self):
        """Тест генерации URL без указания имени"""
        self.teacher1.first_name = ''
        self.teacher1.last_name = ''
        self.teacher1.save()
        
        profile = Profile.objects.create(user=self.teacher1)
        self.assertTrue(profile.custom_url.startswith('nastavnik-'))

    def test_custom_url_uniqueness(self):
        """Тест уникальности URL"""
        # Создаем первый профиль
        profile1 = Profile.objects.create(user=self.teacher1)
        self.assertEqual(profile1.custom_url, 'john-doe')
        
        # Создаем второго учителя с таким же именем
        teacher3 = User.objects.create(
            email='teacher3@example.com',
            first_name='John',
            last_name='Doe',
            role='teacher'
        )
        profile3 = Profile.objects.create(user=teacher3)
        
        # URL должен быть другим
        self.assertNotEqual(profile3.custom_url, profile1.custom_url)
        self.assertTrue(profile3.custom_url.startswith('nastavnik-'))

    def test_student_profile_no_custom_url(self):
        """Тест отсутствия custom_url у студента"""
        profile = Profile.objects.create(user=self.student)
        self.assertIsNone(profile.custom_url)

    def test_get_absolute_url(self):
        """Тест получения абсолютного URL профиля"""
        profile = Profile.objects.create(user=self.teacher1)
        self.assertEqual(profile.get_absolute_url(), f'/{profile.custom_url}/')
        
        # Для профиля без custom_url
        student_profile = Profile.objects.create(user=self.student)
        self.assertEqual(
            student_profile.get_absolute_url(),
            f'/profiles/{self.student.id}/'
        )

    def test_get_courses_url(self):
        """Тест получения URL списка курсов"""
        profile = Profile.objects.create(user=self.teacher1)
        self.assertEqual(
            profile.get_courses_url(),
            f'/{profile.custom_url}/courses/'
        )
        
        # Для профиля без custom_url
        student_profile = Profile.objects.create(user=self.student)
        self.assertEqual(
            student_profile.get_courses_url(),
            f'/profiles/{self.student.id}/courses/'
        )

class TestCustomUrlAPI(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            password='testpass123',
            role='teacher'
        )
        self.client.force_login(self.user)

    def test_check_url_availability(self):
        """Тест проверки доступности URL"""
        # Проверяем свободный URL
        response = self.client.get(
            reverse('check-custom-url') + '?name=test-teacher'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])
        
        # Создаем профиль с этим URL
        Profile.objects.create(
            user=self.user,
            custom_url='test-teacher'
        )
        
        # Проверяем занятый URL
        response = self.client.get(
            reverse('check-custom-url') + '?name=test-teacher'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])

    def test_check_url_without_name(self):
        """Тест проверки URL без указания имени"""
        response = self.client.get(reverse('check-custom-url'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
