from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from accounts.models import ProducerProfile, TeacherProfile
from courses.models import Category, Tag, Course, Module, Lesson

User = get_user_model()

class TestLoadDemoData(TestCase):
    fixtures = ['demo/fixtures/test_demo_data.json']

    def test_producer_exists(self):
        """Проверяем создание продюсера"""
        producer = User.objects.filter(role='producer').first()
        self.assertIsNotNone(producer)
        self.assertEqual(producer.username, 'producer1')
        
        producer_profile = ProducerProfile.objects.first()
        self.assertIsNotNone(producer_profile)
        self.assertEqual(producer_profile.user, producer)

    def test_teachers_exist(self):
        """Проверяем создание учителей"""
        teachers = User.objects.filter(role='teacher')
        self.assertGreater(teachers.count(), 0)
        
        teacher_profiles = TeacherProfile.objects.all()
        self.assertEqual(teacher_profiles.count(), teachers.count())

    def test_courses_exist(self):
        """Проверяем создание курсов и связанных объектов"""
        # Проверяем основные объекты
        self.assertGreater(Category.objects.count(), 0)
        self.assertGreater(Tag.objects.count(), 0)
        self.assertGreater(Course.objects.count(), 0)
        
        # Проверяем первый курс
        course = Course.objects.first()
        self.assertIsNotNone(course)
        self.assertIsNotNone(course.teacher)
        self.assertIsNotNone(course.producer)
        self.assertIsNotNone(course.category)
        
        # Проверяем модули и уроки
        modules = Module.objects.filter(course=course)
        self.assertGreater(modules.count(), 0)
        
        module = modules.first()
        self.assertGreater(Lesson.objects.filter(module=module).count(), 0)
