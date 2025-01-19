from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from accounts.models import ProducerProfile, TeacherProfile, StudentProfile
from courses.models import Category, Tag, Course, Module, Lesson, Review

User = get_user_model()

class TestGenerateData(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Генерируем тестовые данные один раз для всех тестов
        call_command('generate_test_data')

    def test_users_count(self):
        """Проверяем количество созданных пользователей"""
        self.assertEqual(User.objects.filter(role='producer').count(), 20)
        self.assertEqual(User.objects.filter(role='teacher').count(), 50)
        self.assertEqual(User.objects.filter(role='student').count(), 50)

    def test_profiles_count(self):
        """Проверяем количество профилей"""
        self.assertEqual(ProducerProfile.objects.count(), 20)
        self.assertEqual(TeacherProfile.objects.count(), 50)
        self.assertEqual(StudentProfile.objects.count(), 50)

    def test_course_content(self):
        """Проверяем количество курсов и связанного контента"""
        self.assertGreaterEqual(Category.objects.count(), 10)
        self.assertGreaterEqual(Tag.objects.count(), 10)
        self.assertEqual(Course.objects.count(), 100)
        
        # Проверяем что у каждого курса есть модули и уроки
        for course in Course.objects.all():
            self.assertGreaterEqual(Module.objects.filter(course=course).count(), 3)
            for module in Module.objects.filter(course=course):
                self.assertGreaterEqual(Lesson.objects.filter(module=module).count(), 3)

    def test_reviews(self):
        """Проверяем количество отзывов"""
        self.assertEqual(Review.objects.count(), 100)
        
        # Проверяем что отзывы оставлены студентами
        for review in Review.objects.all():
            self.assertEqual(review.user.role, 'student')
            self.assertIsNotNone(review.course)
            self.assertTrue(1 <= review.rating <= 5)

    def test_data_validity(self):
        """Проверяем корректность данных"""
        # Проверяем учителя
        teacher = TeacherProfile.objects.first()
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher.user.role, 'teacher')
        self.assertGreaterEqual(teacher.specializations.count(), 1)
        
        # Проверяем продюсера
        producer = ProducerProfile.objects.first()
        self.assertIsNotNone(producer)
        self.assertEqual(producer.user.role, 'producer')
        self.assertTrue(producer.company)
        
        # Проверяем студента
        student = StudentProfile.objects.first()
        self.assertIsNotNone(student)
        self.assertEqual(student.user.role, 'student')
        self.assertTrue(student.education_level in ['school', 'bachelor', 'master', 'phd'])
        
        # Проверяем курс
        course = Course.objects.first()
        self.assertIsNotNone(course)
        self.assertTrue(course.title)
        self.assertTrue(course.description)
        self.assertIsNotNone(course.teacher)
        self.assertIsNotNone(course.producer)
        self.assertIsNotNone(course.category)
        self.assertGreaterEqual(course.tags.count(), 2)
