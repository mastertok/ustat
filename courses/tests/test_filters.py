import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from courses.models import Course
from accounts.models import User

class TestCourseFilters(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123',
            role='teacher'
        )
        
        # Создаем тестовые курсы
        self.course1 = Course.objects.create(
            title='Python Basic',
            author=self.teacher,
            price=100,
            language='ru',
            duration=30,
            rating=4.5
        )
        
        self.course2 = Course.objects.create(
            title='Python Advanced',
            author=self.teacher,
            price=200,
            language='en',
            duration=60,
            rating=4.8
        )

    def test_price_filter(self):
        """Тест фильтрации по цене"""
        url = reverse('course-list')
        response = self.client.get(url, {'price_min': 150, 'price_max': 250})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Advanced')

    def test_language_filter(self):
        """Тест фильтрации по языку"""
        url = reverse('course-list')
        response = self.client.get(url, {'language': 'ru'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Basic')

    def test_rating_filter(self):
        """Тест фильтрации по рейтингу"""
        url = reverse('course-list')
        response = self.client.get(url, {'rating_min': 4.7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Advanced')

    def test_duration_filter(self):
        """Тест фильтрации по длительности"""
        url = reverse('course-list')
        response = self.client.get(url, {'duration_max': 45})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Basic')

    def test_multiple_filters(self):
        """Тест комбинированной фильтрации"""
        url = reverse('course-list')
        response = self.client.get(url, {
            'price_min': 50,
            'price_max': 150,
            'language': 'ru',
            'rating_min': 4.0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Basic')

    def test_empty_filter_results(self):
        """Тест пустых результатов фильтрации"""
        url = reverse('course-list')
        response = self.client.get(url, {'price_min': 1000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_invalid_filter_values(self):
        """Тест некорректных значений фильтров"""
        url = reverse('course-list')
        response = self.client.get(url, {'price_min': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
