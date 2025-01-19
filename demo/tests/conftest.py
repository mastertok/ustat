import pytest
from django.core.management import call_command
from django.db import connection

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Настройка базы данных для тестов"""
    with django_db_blocker.unblock():
        # Применяем миграции перед запуском тестов
        call_command('migrate')

@pytest.fixture(autouse=True)
def clean_database(django_db_blocker):
    """Очищаем базу данных перед каждым тестом"""
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            # Отключаем внешние ключи для SQLite
            cursor.execute("PRAGMA foreign_keys = OFF;")
            
            # Получаем список всех таблиц
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
            tables = cursor.fetchall()
            
            # Очищаем каждую таблицу
            for table in tables:
                if table[0] != 'django_migrations':
                    cursor.execute(f"DELETE FROM {table[0]};")
            
            # Включаем внешние ключи
            cursor.execute("PRAGMA foreign_keys = ON;")

@pytest.fixture
def admin_user(db):
    """Фикстура для создания админа"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin12345',
        role='admin'
    )
    return admin

@pytest.fixture
def teacher_user(db):
    """Фикстура для создания учителя"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    teacher = User.objects.create_user(
        username='teacher1',
        email='teacher1@example.com',
        password='password123',
        role='teacher',
        first_name='Иван',
        last_name='Петров'
    )
    return teacher

@pytest.fixture
def student_user(db):
    """Фикстура для создания студента"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    student = User.objects.create_user(
        username='student1',
        email='student1@example.com',
        password='password123',
        role='student',
        first_name='Алексей',
        last_name='Иванов'
    )
    return student

@pytest.fixture
def producer_user(db):
    """Фикстура для создания продюсера"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    producer = User.objects.create_user(
        username='producer1',
        email='producer1@example.com',
        password='password123',
        role='producer',
        first_name='Сергей',
        last_name='Сидоров'
    )
    return producer
