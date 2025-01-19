from django.contrib.auth import get_user_model
from accounts.models import ProducerProfile, TeacherProfile, Specialization
from courses.models import Category, Tag, Course, Module, Lesson

User = get_user_model()

def create_producer():
    """Создает тестового продюсера"""
    producer = User.objects.create_user(
        username='producer1',
        email='producer1@example.com',
        password='producer12345',
        first_name='Продюсер',
        last_name='Тестовый',
        role='producer',
        bio='Главный продюсер образовательной платформы',
        phone='+996700333333'
    )
    producer_profile = ProducerProfile.objects.create(
        user=producer,
        company='Education Production'
    )
    return producer_profile

def create_teacher(username='teacher1', first_name='Иван', last_name='Петров'):
    """Создает тестового учителя"""
    teacher = User.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password='teacher12345',
        first_name=first_name,
        last_name=last_name,
        role='teacher',
        bio='Опытный преподаватель',
        phone='+996700111111'
    )
    specialization = Specialization.objects.create(
        name='Математика',
        slug='mathematics',
        description='Специализация в области математики'
    )
    teacher_profile = TeacherProfile.objects.create(
        user=teacher,
        experience_summary='10 лет опыта преподавания',
        education_summary='МГУ, Факультет математики',
        teaching_style='Индивидуальный подход',
        slug=f'teacher-{username}'
    )
    teacher_profile.specializations.add(specialization)
    return teacher_profile

def create_course(teacher_profile, producer_profile):
    """Создает тестовый курс"""
    category = Category.objects.create(
        name='Математика',
        slug='mathematics',
        description='Курсы по математике'
    )
    
    tag1 = Tag.objects.create(name='Для начинающих', slug='for-beginners')
    tag2 = Tag.objects.create(name='Теория', slug='theory')
    
    course = Course.objects.create(
        title='Алгебра для начинающих',
        slug='algebra-for-beginners',
        description='Базовый курс алгебры',
        excerpt='Научитесь основам алгебры',
        category=category,
        teacher=teacher_profile,
        producer=producer_profile,
        max_students=50,
        difficulty_level='beginner',
        language='ru',
        duration_minutes=1200,
        enable_qa=True,
        enable_announcements=True,
        enable_reviews=True,
        course_type='paid',
        price='5000.00',
        currency='KGS',
        status='published'
    )
    course.tags.add(tag1, tag2)
    
    # Создаем модули
    module = Module.objects.create(
        course=course,
        title='Введение в алгебру',
        description='Базовые понятия алгебры',
        order=1
    )
    
    # Создаем уроки
    Lesson.objects.create(
        module=module,
        title='Что такое алгебра',
        content_type='video',
        content='<p>Содержание урока</p>',
        order=1,
        duration_minutes=45
    )
    
    return course
