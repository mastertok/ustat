import pytest
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from accounts.models import TeacherProfile, ProducerProfile
from courses.models import Course

User = get_user_model()

@pytest.mark.django_db
class TestLoadDemoDataCommand:
    def test_load_demo_data_idempotent(self):
        """
        Проверяем, что команда может быть выполнена несколько раз без ошибок
        """
        # Первый запуск
        call_command('load_demo_data_v2')
        
        # Запоминаем количество объектов после первого запуска
        initial_users = User.objects.count()
        initial_teachers = TeacherProfile.objects.count()
        initial_courses = Course.objects.count()
        
        # Второй запуск
        call_command('load_demo_data_v2')
        
        # Проверяем, что количество объектов не изменилось
        assert User.objects.count() == initial_users
        assert TeacherProfile.objects.count() == initial_teachers
        assert Course.objects.count() == initial_courses

    def test_load_demo_data_admin_creation(self):
        """
        Проверяем создание администратора
        """
        call_command('load_demo_data_v2')
        
        admin = User.objects.get(username='admin')
        assert admin.is_superuser
        assert admin.is_staff
        assert admin.role == 'admin'

    def test_load_demo_data_relationships(self):
        """
        Проверяем корректность связей между объектами
        """
        call_command('load_demo_data_v2')
        
        # Проверяем связи учитель-курс-продюсер
        for course in Course.objects.all():
            assert course.teacher is not None
            assert course.producer is not None
            assert isinstance(course.teacher, TeacherProfile)
            assert isinstance(course.producer, ProducerProfile)
            
            # Проверяем, что учитель и продюсер имеют правильные роли
            assert course.teacher.user.role == 'teacher'
            assert course.producer.user.role == 'producer'

    def test_load_demo_data_constraints(self):
        """
        Проверяем, что ограничения уникальности соблюдаются
        """
        call_command('load_demo_data_v2')
        
        # Проверяем уникальность slug у учителей
        teacher_slugs = TeacherProfile.objects.values_list('slug', flat=True)
        assert len(teacher_slugs) == len(set(teacher_slugs))
        
        # Проверяем уникальность slug у курсов
        course_slugs = Course.objects.values_list('slug', flat=True)
        assert len(course_slugs) == len(set(course_slugs))
        
        # Проверяем, что нельзя создать дубликат с тем же slug
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                Course.objects.create(
                    title=Course.objects.first().title,
                    slug=Course.objects.first().slug,
                    teacher=TeacherProfile.objects.first(),
                    producer=ProducerProfile.objects.first()
                )

    def test_load_demo_data_cleanup(self):
        """
        Проверяем, что старые данные очищаются перед загрузкой новых
        """
        # Создаем тестового пользователя
        User.objects.create_user(
            username='test_user',
            password='test_password',
            role='student'
        )
        
        # Запускаем загрузку демо-данных
        call_command('load_demo_data_v2')
        
        # Проверяем, что тестовый пользователь был удален
        assert not User.objects.filter(username='test_user').exists()
        
        # Проверяем, что админ существует
        assert User.objects.filter(username='admin').exists()
