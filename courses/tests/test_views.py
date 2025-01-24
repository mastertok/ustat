import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User
from courses.models import Course, Category, Module, Lesson

class TestCourseViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Создаем пользователей с разными ролями
        self.student = User.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123',
            role='teacher'
        )
        
        self.producer = User.objects.create_user(
            email='producer@example.com',
            password='testpass123',
            role='producer'
        )
        
        # Создаем тестовые данные
        self.category = Category.objects.create(
            name='Programming',
            slug='programming'
        )
        
        self.course1 = Course.objects.create(
            title='Python Basic',
            slug='python-basic',
            description='Learn Python basics',
            category=self.category,
            price=100,
            language='ru',
            duration=30,
            status='published',
            average_rating=4.5
        )
        
        self.course2 = Course.objects.create(
            title='Python Advanced',
            slug='python-advanced',
            description='Advanced Python topics',
            category=self.category,
            price=200,
            language='en',
            duration=60,
            status='published',
            average_rating=4.8
        )

    def test_course_list(self):
        """Тест получения списка курсов"""
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_course_filters(self):
        """Тест фильтрации курсов"""
        url = reverse('course-list')
        
        # Тест фильтрации по цене
        response = self.client.get(url, {'price_min': 150})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Advanced')
        
        # Тест фильтрации по языку
        response = self.client.get(url, {'language': 'ru'})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Basic')

    def test_course_search(self):
        """Тест поиска курсов"""
        url = reverse('course-list')
        response = self.client.get(url, {'search': 'Advanced'})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Advanced')

    def test_course_ordering(self):
        """Тест сортировки курсов"""
        url = reverse('course-list')
        
        # Сортировка по цене (по возрастанию)
        response = self.client.get(url, {'ordering': 'price'})
        self.assertEqual(response.data['results'][0]['title'], 'Python Basic')
        
        # Сортировка по рейтингу (по убыванию)
        response = self.client.get(url, {'ordering': '-average_rating'})
        self.assertEqual(response.data['results'][0]['title'], 'Python Advanced')

    def test_course_create_permissions(self):
        """Тест прав доступа при создании курса"""
        url = reverse('course-list')
        data = {
            'title': 'New Course',
            'description': 'Course description',
            'category': self.category.id,
            'price': 150,
            'language': 'ru',
            'duration': 45
        }
        
        # Неавторизованный пользователь
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Студент
        self.client.force_authenticate(user=self.student)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Преподаватель
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recommended_courses(self):
        """Тест получения рекомендованных курсов"""
        url = reverse('course-recommended')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Оба курса имеют рейтинг > 4.0

    def test_price_ranges(self):
        """Тест получения диапазонов цен"""
        url = reverse('course-price-ranges')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['min_price'], '100.00')
        self.assertEqual(response.data['max_price'], '200.00')
