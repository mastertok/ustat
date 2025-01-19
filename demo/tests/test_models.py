import pytest
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from accounts.models import TeacherProfile, Education, WorkExperience, Achievement, Specialization
from courses.models import Course, Category, Enrollment
from reviews.models import Review, Reply
import uuid

User = get_user_model()

def get_unique_username():
    """Генерирует уникальное имя пользователя"""
    return f"user_{uuid.uuid4().hex[:8]}"

def get_unique_slug():
    """Генерирует уникальный slug"""
    return f"slug_{uuid.uuid4().hex[:8]}"

@pytest.fixture
def demo_data(db, django_db_setup):
    """Фикстура для загрузки демо-данных"""
    call_command('load_demo_data_v2')

@pytest.mark.django_db
class TestTeacherProfile:
    def test_teacher_profile_creation(self, teacher_user):
        """Тест создания профиля учителя"""
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            experience_summary='10 лет опыта преподавания',
            achievements_summary='Множество наград',
            education_summary='Высшее образование',
            teaching_style='Индивидуальный подход',
            slug=get_unique_slug()
        )
        
        assert profile.experience_summary == '10 лет опыта преподавания'
        assert profile.rating == 0
        assert profile.students_count == 0
        assert profile.reviews_count == 0
    
    def test_teacher_specializations(self, teacher_user):
        """Тест добавления специализаций учителю"""
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        spec = Specialization.objects.create(
            name='Математика',
            description='Высшая математика',
            slug=get_unique_slug()
        )
        
        profile.specializations.add(spec)
        assert profile.specializations.count() == 1
        assert profile.specializations.first().name == 'Математика'

    def test_teacher_education(self, teacher_user):
        """Тест добавления образования учителю"""
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        education = Education.objects.create(
            teacher=profile,
            institution='КНУ',
            degree='Бакалавр',
            field_of_study='Математика',
            start_date='2015-09-01',
            end_date='2019-06-30',
            description='Отличник'
        )
        
        assert profile.education_records.count() == 1
        edu = profile.education_records.first()
        assert edu.institution == 'КНУ'
        assert edu.degree == 'Бакалавр'
    
    def test_teacher_work_experience(self, teacher_user):
        """Тест добавления опыта работы учителю"""
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        work = WorkExperience.objects.create(
            teacher=profile,
            company='Школа №1',
            position='Учитель математики',
            start_date='2019-09-01',
            is_current=True,
            description='Преподавание математики'
        )
        
        assert profile.work_experiences.count() == 1
        exp = profile.work_experiences.first()
        assert exp.company == 'Школа №1'
        assert exp.is_current is True
    
    def test_teacher_achievements(self, teacher_user):
        """Тест добавления достижений учителю"""
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        achievement = Achievement.objects.create(
            teacher=profile,
            title='Лучший учитель года',
            date_received='2023-05-15',
            issuer='Министерство образования',
            description='За выдающиеся достижения'
        )
        
        assert profile.achievement_records.count() == 1
        ach = profile.achievement_records.first()
        assert ach.title == 'Лучший учитель года'
        assert ach.issuer == 'Министерство образования'

@pytest.mark.django_db
class TestDemoData:
    """Тесты для проверки демо-данных"""
    
    def test_demo_data_loaded(self, demo_data):
        """Проверка загрузки всех демо-данных"""
        # Проверяем количество созданных объектов
        assert User.objects.count() > 0
        assert TeacherProfile.objects.count() == 5
        assert Course.objects.count() == 5
        assert Education.objects.count() == 5
        assert WorkExperience.objects.count() == 5
        assert Achievement.objects.count() == 5
        
        # Проверяем связи
        for teacher in TeacherProfile.objects.all():
            assert teacher.education_records.exists()
            assert teacher.work_experiences.exists()
            assert teacher.achievement_records.exists()
            assert teacher.specializations.exists()
            
        # Проверяем курсы
        for course in Course.objects.all():
            assert course.teacher is not None
            assert course.producer is not None
            assert course.category is not None
            
        # Проверяем записи и отзывы
        assert Enrollment.objects.count() > 0
        assert Review.objects.count() > 0
        assert Reply.objects.count() > 0
