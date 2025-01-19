import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Course, Category

User = get_user_model()

class TestCourseSEO(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Программирование',
            description='Курсы программирования',
            icon='code'
        )
        
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов'
        )

    def test_auto_generate_seo_fields(self):
        """Тест автоматической генерации SEO полей"""
        course = Course.objects.create(
            title='Python для начинающих',
            description='Полный курс Python для начинающих программистов',
            price=10000,
            level='beginner',
            language='ru',
            duration='2 месяца',
            category=self.category,
            instructor=self.instructor
        )
        
        # Проверяем, что slug сгенерирован автоматически
        self.assertEqual(course.slug, 'python-dlya-nachinayushchikh')
        
        # Проверяем автоматическую генерацию meta_title
        self.assertEqual(course.meta_title, 'Python для начинающих')
        
        # Проверяем, что meta_description ограничен 160 символами
        self.assertTrue(len(course.meta_description) <= 160)
        self.assertTrue(course.meta_description.startswith('Полный курс Python'))
        
        # Проверяем генерацию ключевых слов
        expected_keywords = [
            'Python для начинающих',
            'Программирование',
            'beginner',
            'онлайн курс',
            'обучение'
        ]
        for keyword in expected_keywords:
            self.assertIn(keyword, course.meta_keywords)

    def test_custom_seo_fields(self):
        """Тест сохранения пользовательских SEO полей"""
        custom_meta_title = 'Изучите Python за 2 месяца'
        custom_meta_description = 'Лучший курс Python для новичков'
        custom_meta_keywords = 'python, программирование, обучение, разработка'
        
        course = Course.objects.create(
            title='Python для начинающих',
            description='Полный курс Python для начинающих программистов',
            price=10000,
            level='beginner',
            language='ru',
            duration='2 месяца',
            category=self.category,
            instructor=self.instructor,
            meta_title=custom_meta_title,
            meta_description=custom_meta_description,
            meta_keywords=custom_meta_keywords
        )
        
        # Проверяем, что пользовательские SEO поля сохранены
        self.assertEqual(course.meta_title, custom_meta_title)
        self.assertEqual(course.meta_description, custom_meta_description)
        self.assertEqual(course.meta_keywords, custom_meta_keywords)

    def test_update_seo_fields(self):
        """Тест обновления SEO полей"""
        course = Course.objects.create(
            title='Python для начинающих',
            description='Полный курс Python для начинающих программистов',
            price=10000,
            level='beginner',
            language='ru',
            duration='2 месяца',
            category=self.category,
            instructor=self.instructor
        )
        
        # Обновляем SEO поля
        new_meta_title = 'Новый SEO заголовок'
        new_meta_description = 'Новое SEO описание'
        new_meta_keywords = 'новые, ключевые, слова'
        
        course.meta_title = new_meta_title
        course.meta_description = new_meta_description
        course.meta_keywords = new_meta_keywords
        course.save()
        
        # Перезагружаем курс из базы данных
        course.refresh_from_db()
        
        # Проверяем, что SEO поля обновились
        self.assertEqual(course.meta_title, new_meta_title)
        self.assertEqual(course.meta_description, new_meta_description)
        self.assertEqual(course.meta_keywords, new_meta_keywords)

    def test_empty_seo_fields_validation(self):
        """Тест валидации пустых SEO полей"""
        course = Course.objects.create(
            title='Python для начинающих',
            description='Полный курс Python для начинающих программистов',
            price=10000,
            level='beginner',
            language='ru',
            duration='2 месяца',
            category=self.category,
            instructor=self.instructor,
            meta_title='',
            meta_description='',
            meta_keywords=''
        )
        
        # Проверяем, что пустые поля заполнились автоматически
        self.assertNotEqual(course.meta_title, '')
        self.assertNotEqual(course.meta_description, '')
        self.assertNotEqual(course.meta_keywords, '')
