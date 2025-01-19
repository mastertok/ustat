from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files import File
from accounts.models import TeacherProfile, Achievement, Education, WorkExperience, ProducerProfile, Specialization
from courses.models import Course, Module, Lesson, Announcement, Category, Tag
from reviews.models import Review
from faker import Faker
import random
import os
from django.utils.text import slugify
from django.db import transaction
from django.db.models.signals import post_save
from accounts.signals import create_teacher_profile

User = get_user_model()
fake = Faker(['ru_RU'])

class Command(BaseCommand):
    help = 'Generates demo data for courses, modules, lessons, and teacher profiles'

    def handle(self, *args, **options):
        try:
            # Отключаем сигнал создания профиля учителя
            post_save.disconnect(create_teacher_profile, sender=User)

            with transaction.atomic():
                # Очищаем существующие данные
                self.stdout.write('Очищаем существующие данные...')
                Course.objects.all().delete()
                Module.objects.all().delete()
                Lesson.objects.all().delete()
                Announcement.objects.all().delete()
                Achievement.objects.all().delete()
                Education.objects.all().delete()
                WorkExperience.objects.all().delete()
                Category.objects.all().delete()
                Tag.objects.all().delete()
                Review.objects.all().delete()
                TeacherProfile.objects.all().delete()
                ProducerProfile.objects.all().delete()
                User.objects.filter(is_superuser=False).delete()
                Specialization.objects.all().delete()

                # Создаем специализации
                self.stdout.write('Создаем специализации...')
                specializations = []
                specialization_names = [
                    'Веб-разработка', 'Мобильная разработка', 'Data Science', 
                    'UI/UX Дизайн', 'Графический дизайн', 'Маркетинг', 
                    'SEO-оптимизация', 'SMM', 'Копирайтинг', 'Контент-маркетинг',
                    'Английский язык', 'Китайский язык', 'Математика', 
                    'Физика', 'Химия', 'Биология', 'История', 'Философия',
                    'Психология', 'Экономика'
                ]
                for i, name in enumerate(specialization_names, 1):
                    specialization = Specialization.objects.create(
                        name=name,
                        slug=f"{slugify(name)}-{i}",
                        description=fake.text(max_nb_chars=200)
                    )
                    specializations.append(specialization)
                    self.stdout.write(f'Создана специализация: {specialization.name}')

                # Создаем пользователей
                self.stdout.write('Создаем пользователей...')
                students = []
                for i in range(40):  # 40 студентов
                    user = User.objects.create_user(
                        username=f'student{i+1}',
                        email=f'student{i+1}@example.com',
                        password='student12345',
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        role='student'
                    )
                    students.append(user)
                    self.stdout.write(f'Создан студент: {user.get_full_name()}')

                producers = []
                for i in range(30):  # 30 продюсеров
                    user = User.objects.create_user(
                        username=f'producer{i+1}',
                        email=f'producer{i+1}@example.com',
                        password='producer12345',
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        role='producer'
                    )
                    producer_profile = ProducerProfile.objects.create(
                        user=user,
                        company=fake.company(),
                        portfolio=fake.url()
                    )
                    producers.append(user)
                    self.stdout.write(f'Создан продюсер: {user.get_full_name()}')

                teachers = []
                for i in range(50):  # 50 учителей
                    user = User.objects.create_user(
                        username=f'teacher{i+1}',
                        email=f'teacher{i+1}@example.com',
                        password='teacher12345',
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        role='teacher'
                    )
                    teacher_profile = TeacherProfile.objects.create(
                        user=user,
                        experience_summary=fake.text(max_nb_chars=200),
                        education_summary=fake.text(max_nb_chars=200),
                        teaching_style=fake.text(max_nb_chars=100),
                        slug=f'teacher-{i+1}'
                    )
                    # Добавляем случайные специализации
                    teacher_profile.specializations.add(*random.sample(specializations, k=random.randint(1, 3)))
                    teachers.append(user)
                    self.stdout.write(f'Создан учитель: {user.get_full_name()}')

                # Создаем категории
                self.stdout.write('Создаем категории...')
                categories = []
                category_names = [
                    'Программирование', 'Дизайн', 'Бизнес', 'Маркетинг', 
                    'Иностранные языки', 'Музыка', 'Фотография', 'Саморазвитие',
                    'Математика', 'Физика'
                ]
                for i, name in enumerate(category_names, 1):
                    category = Category.objects.create(
                        name=name,
                        slug=f"{slugify(name)}-{i}",
                        description=fake.text(max_nb_chars=200)
                    )
                    categories.append(category)
                    self.stdout.write(f'Создана категория: {category.name}')

                # Создаем теги
                self.stdout.write('Создаем теги...')
                tags = []
                tag_names = [
                    'Для начинающих', 'Продвинутый уровень', 'Практика', 
                    'Теория', 'Интенсив', 'С нуля', 'Мастер-класс', 'Для детей'
                ]
                for i, name in enumerate(tag_names, 1):
                    tag = Tag.objects.create(
                        name=name,
                        slug=f"{slugify(name)}-{i}"
                    )
                    tags.append(tag)
                    self.stdout.write(f'Создан тег: {tag.name}')

                # Создаем курсы для каждого учителя
                self.stdout.write('Создаем курсы...')
                courses = []
                for teacher in teachers:
                    for i in range(random.randint(1, 3)):  # 1-3 курса на учителя
                        course = Course.objects.create(
                            title=f"{fake.word().capitalize()} {fake.word()}",
                            slug=f"course-{len(courses)+1}",
                            description=fake.text(max_nb_chars=500),
                            excerpt=fake.text(max_nb_chars=200),
                            teacher=teacher.teacher_profile,
                            category=random.choice(categories),
                            max_students=random.randint(20, 100),
                            difficulty_level=random.choice(['beginner', 'intermediate', 'advanced']),
                            language=random.choice(['ru', 'ky', 'en']),
                            duration_minutes=random.randint(600, 4800),
                            enable_qa=True,
                            enable_announcements=True,
                            enable_reviews=True,
                            course_type=random.choice(['free', 'paid']),
                            price=str(random.randint(3000, 15000)) + ".00",
                            currency="KGS",
                            status="published",
                            published_at=timezone.now()
                        )
                        # Добавляем случайные теги
                        course.tags.add(*random.sample(tags, k=random.randint(2, 4)))
                        courses.append(course)
                        self.stdout.write(f'Создан курс: {course.title}')

                # Создаем отзывы
                self.stdout.write('Создаем отзывы...')
                for i in range(50):  # 50 отзывов
                    course = random.choice(courses)
                    student = random.choice(students)
                    review = Review.objects.create(
                        course=course,
                        user=student,
                        rating=random.randint(3, 5),
                        comment=fake.text(max_nb_chars=200)
                    )
                    self.stdout.write(f'Создан отзыв для курса {course.title} от {student.get_full_name()}')

                # Создаем модули
                self.stdout.write('Создаем модули...')
                modules = []
                for course in courses:
                    for i in range(5):  # 5 модулей на курс
                        module = Module.objects.create(
                            course=course,
                            title=f"Модуль {i+1}: {fake.word().capitalize()}",
                            description=fake.text(max_nb_chars=200),
                            order=i+1
                        )
                        modules.append(module)
                        self.stdout.write(f'Создан модуль: {module.title}')

                # Создаем уроки
                self.stdout.write('Создаем уроки...')
                for module in modules:
                    for i in range(6):  # 6 уроков на модуль
                        lesson = Lesson.objects.create(
                            module=module,
                            title=f"Урок {i+1}: {fake.word().capitalize()}",
                            content_type=random.choice(['video', 'text', 'test', 'presentation']),
                            content=fake.text(max_nb_chars=300),
                            order=i+1,
                            duration_minutes=random.randint(30, 90)
                        )
                        self.stdout.write(f'Создан урок: {lesson.title}')

                # Создаем объявления
                self.stdout.write('Создаем объявления...')
                for course in courses:
                    for i in range(random.randint(1, 3)):  # 1-3 объявления на курс
                        announcement = Announcement.objects.create(
                            course=course,
                            title=f"Объявление: {fake.sentence()}",
                            content=fake.text(max_nb_chars=500),
                            created_at=timezone.now()
                        )
                        self.stdout.write(f'Создано объявление: {announcement.title}')

                # Создаем достижения для учителей
                self.stdout.write('Создаем достижения...')
                for teacher in teachers:
                    for i in range(random.randint(1, 3)):  # 1-3 достижения на учителя
                        achievement = Achievement.objects.create(
                            teacher=teacher.teacher_profile,
                            title=f"Достижение: {fake.sentence()}",
                            date_received=fake.date_between(start_date='-5y', end_date='today'),
                            issuer=fake.company(),
                            description=fake.text(max_nb_chars=200)
                        )
                        self.stdout.write(f'Создано достижение: {achievement.title}')

                # Создаем образование для учителей
                self.stdout.write('Создаем образование...')
                for teacher in teachers:
                    for i in range(random.randint(1, 3)):  # 1-3 записи об образовании на учителя
                        education = Education.objects.create(
                            teacher=teacher.teacher_profile,
                            institution=fake.company(),
                            degree=random.choice(['Бакалавр', 'Магистр', 'PhD']),
                            field_of_study=fake.job(),
                            start_date=fake.date_between(start_date='-10y', end_date='-5y'),
                            end_date=fake.date_between(start_date='-5y', end_date='-1y'),
                            description=fake.text(max_nb_chars=200)
                        )
                        self.stdout.write(f'Создано образование: {education.degree} в {education.institution}')

                # Создаем опыт работы для учителей
                self.stdout.write('Создаем опыт работы...')
                for teacher in teachers:
                    for i in range(random.randint(1, 3)):  # 1-3 записи об опыте работы на учителя
                        is_current = i == 0
                        work_exp = WorkExperience.objects.create(
                            teacher=teacher.teacher_profile,
                            company=fake.company(),
                            position=fake.job(),
                            start_date=fake.date_between(start_date='-10y', end_date='-1y'),
                            end_date=None if is_current else fake.date_between(start_date='-1y', end_date='today'),
                            description=fake.text(max_nb_chars=200),
                            is_current=is_current
                        )
                        self.stdout.write(f'Создан опыт работы: {work_exp.position} в {work_exp.company}')

                self.stdout.write(self.style.SUCCESS('\nДемо данные успешно сгенерированы\n'))
                
                # Выводим статистику
                self.stdout.write('Статистика:')
                self.stdout.write(f'Специализаций: {Specialization.objects.count()}')
                self.stdout.write(f'Студентов: {User.objects.filter(role="student").count()}')
                self.stdout.write(f'Продюсеров: {User.objects.filter(role="producer").count()}')
                self.stdout.write(f'Учителей: {User.objects.filter(role="teacher").count()}')
                self.stdout.write(f'Категорий: {Category.objects.count()}')
                self.stdout.write(f'Тегов: {Tag.objects.count()}')
                self.stdout.write(f'Курсов: {Course.objects.count()}')
                self.stdout.write(f'Модулей: {Module.objects.count()}')
                self.stdout.write(f'Уроков: {Lesson.objects.count()}')
                self.stdout.write(f'Объявлений: {Announcement.objects.count()}')
                self.stdout.write(f'Отзывов: {Review.objects.count()}')
                self.stdout.write(f'Достижений: {Achievement.objects.count()}')
                self.stdout.write(f'Записей об образовании: {Education.objects.count()}')
                self.stdout.write(f'Записей об опыте работы: {WorkExperience.objects.count()}')

            # Восстанавливаем сигнал создания профиля учителя
            post_save.connect(create_teacher_profile, sender=User)

        except Exception as e:
            # Восстанавливаем сигнал создания профиля учителя в случае ошибки
            post_save.connect(create_teacher_profile, sender=User)
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {str(e)}'))
