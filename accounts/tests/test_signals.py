import pytest
from django.test import TestCase
from accounts.models import User, TeacherProfile

class TestTeacherProfileSignals(TestCase):
    def test_teacher_profile_created_on_user_creation(self):
        """
        Тест проверяет, что профиль учителя создается автоматически
        при регистрации пользователя с ролью teacher
        """
        # Создаем тестового пользователя-учителя
        teacher = User.objects.create_user(
            username='test_teacher',
            email='teacher@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Teacher',
            role='teacher'
        )
        
        # Проверяем, что профиль учителя был создан
        self.assertTrue(TeacherProfile.objects.filter(user=teacher).exists())
        
        # Проверяем правильность slug
        profile = TeacherProfile.objects.get(user=teacher)
        self.assertEqual(profile.slug, 'test-teacher')

    def test_profile_not_created_for_student(self):
        """
        Тест проверяет, что профиль учителя НЕ создается
        при регистрации обычного пользователя
        """
        # Создаем тестового пользователя-студента
        student = User.objects.create_user(
            username='test_student',
            email='student@test.com',
            password='testpass123',
            role='student'
        )
        
        # Проверяем, что профиль учителя НЕ был создан
        self.assertFalse(TeacherProfile.objects.filter(user=student).exists())
