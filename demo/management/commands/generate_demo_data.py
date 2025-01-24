import json
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import (
    Specialization, TeacherProfile, Education, WorkExperience, 
    Achievement, StudentProfile, ProducerProfile
)
from courses.models import (
    Category, Tag, Course, Module, Lesson, Review, Announcement,
    Enrollment, Promocode, Promotion, CourseAnalytics, TrafficSource,
    EmailCampaign
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Генерирует расширенный набор демо-данных'

    def generate_users(self, num_users=100):
        users = []
        # Создаем фиксированное количество пользователей каждой роли
        for i in range(num_users):
            if i < 70:  # Первые 70 - студенты
                role = 'student'
            elif i < 90:  # Следующие 20 - учителя
                role = 'teacher'
            else:  # Последние 10 - продюсеры
                role = 'producer'
            
            user = {
                "model": "accounts.user",
                "pk": i + 100,
                "fields": {
                    "password": "pbkdf2_sha256$600000$default$password",
                    "is_superuser": False,
                    "username": f"{role}{i}",
                    "first_name": f"Имя{i}",
                    "last_name": f"Фамилия{i}",
                    "email": f"{role}{i}@ustat.kg",
                    "is_staff": False,
                    "is_active": True,
                    "date_joined": timezone.now().isoformat(),
                    "role": role,
                    "bio": f"Биография пользователя {i}",
                    "phone": f"+99670000{i:04d}",
                    "groups": [],
                    "user_permissions": []
                }
            }
            users.append(user)
        return users

    def generate_specializations(self, num_specs=20):
        specs = []
        subjects = [
            "Математика", "Физика", "Химия", "Биология", "История",
            "География", "Литература", "Английский язык", "Программирование",
            "Экономика", "Психология", "Философия", "Социология", "Право",
            "Маркетинг", "Дизайн", "Музыка", "Искусство", "Спорт", "Медицина"
        ]
        for i, subject in enumerate(subjects[:num_specs]):
            spec = {
                "model": "accounts.specialization",
                "pk": i + 100,
                "fields": {
                    "name": subject,
                    "description": f"Преподавание {subject.lower()}",
                    "slug": self.slugify_ru(subject)
                }
            }
            specs.append(spec)
        return specs

    def generate_teacher_profiles(self, num_profiles=20):
        profiles = []
        # Генерируем профили только для учителей (ID от 170 до 189)
        for i in range(num_profiles):
            teacher_id = 170 + i  # ID пользователей-учителей
            profile = {
                "model": "accounts.teacherprofile",
                "pk": i + 100,
                "fields": {
                    "user": teacher_id,
                    "experience_summary": f"Опыт преподавания {random.randint(1, 20)} лет",
                    "achievements_summary": "Различные достижения и награды",
                    "education_summary": "Высшее образование",
                    "rating": str(round(random.uniform(4.0, 5.0), 2)),
                    "students_count": random.randint(10, 1000),
                    "reviews_count": random.randint(5, 100),
                    "social_links": {
                        "facebook": f"https://facebook.com/teacher{i}",
                        "linkedin": f"https://linkedin.com/in/teacher{i}"
                    },
                    "teaching_style": "Индивидуальный подход к каждому ученику",
                    "slug": f"teacher-{i}",
                    "created_at": timezone.now().isoformat(),
                    "updated_at": timezone.now().isoformat()
                }
            }
            profiles.append(profile)
        return profiles

    def generate_student_profiles(self, num_profiles=70):
        profiles = []
        # Генерируем профили только для студентов (ID от 100 до 169)
        for i in range(num_profiles):
            student_id = 100 + i  # ID пользователей-студентов
            profile = {
                "model": "accounts.studentprofile",
                "pk": i + 100,
                "fields": {
                    "user": student_id,
                    "interests": f"Интересы студента {i}",
                    "education_level": random.choice(['school', 'bachelor', 'master', 'phd'])
                }
            }
            profiles.append(profile)
        return profiles

    def generate_producer_profiles(self, num_profiles=10):
        profiles = []
        # Генерируем профили только для продюсеров (ID от 190 до 199)
        for i in range(num_profiles):
            producer_id = 190 + i  # ID пользователей-продюсеров
            profile = {
                "model": "accounts.producerprofile",
                "pk": i + 100,
                "fields": {
                    "user": producer_id,
                    "company": f"Компания {i}",
                    "portfolio": f"https://portfolio.com/producer{i}"
                }
            }
            profiles.append(profile)
        return profiles

    def generate_courses(self, num_courses=100):
        courses = []
        for i in range(num_courses):
            course = {
                "model": "courses.course",
                "pk": i + 100,
                "fields": {
                    "title": f"Курс {i}",
                    "slug": f"course-{i}",
                    "description": f"Описание курса {i}",
                    "excerpt": f"Краткое описание курса {i}",
                    "category": random.randint(1, 10),
                    "teacher": random.randint(170, 189),  # ID учителей
                    "producer": None,
                    "cover_image": "",
                    "video_intro": None,
                    "max_students": random.randint(50, 200),
                    "difficulty_level": random.choice(["beginner", "intermediate", "advanced"]),
                    "language": random.choice(["ky", "ru"]),
                    "duration_minutes": random.randint(600, 3600),
                    "enable_qa": True,
                    "enable_announcements": True,
                    "enable_reviews": True,
                    "course_type": random.choice(["free", "paid"]),
                    "price": str(random.randint(1000, 10000)) + ".00",
                    "currency": "KGS",
                    "discount_price": None,
                    "sales_count": random.randint(0, 100),
                    "average_rating": str(round(random.uniform(4.0, 5.0), 2)),
                    "reviews_count": random.randint(0, 50),
                    "status": "published",
                    "created_at": timezone.now().isoformat(),
                    "updated_at": timezone.now().isoformat(),
                    "published_at": timezone.now().isoformat(),
                    "tags": [random.randint(1, 10) for _ in range(random.randint(1, 3))]
                }
            }
            courses.append(course)
        return courses

    def generate_modules(self, num_modules=300):
        modules = []
        for i in range(num_modules):
            module = {
                "model": "courses.module",
                "pk": i + 100,
                "fields": {
                    "course": random.randint(100, 199),  # ID курсов
                    "title": f"Модуль {i}",
                    "description": f"Описание модуля {i}",
                    "order": random.randint(1, 10)
                }
            }
            modules.append(module)
        return modules

    def generate_lessons(self, num_lessons=1000):
        lessons = []
        content_types = ["video", "text", "test", "presentation"]
        for i in range(num_lessons):
            content_type = random.choice(content_types)
            lesson = {
                "model": "courses.lesson",
                "pk": i + 100,
                "fields": {
                    "module": random.randint(100, 399),  # ID модулей
                    "title": f"Урок {i}",
                    "content_type": content_type,
                    "content": f"Содержание урока {i}",
                    "video_url": f"https://youtube.com/watch?v=example{i}" if content_type == "video" else None,
                    "order": random.randint(1, 10),
                    "duration_minutes": random.randint(15, 90)
                }
            }
            lessons.append(lesson)
        return lessons

    def generate_reviews(self, num_reviews=500):
        reviews = []
        for i in range(num_reviews):
            review = {
                "model": "courses.review",
                "pk": i + 100,
                "fields": {
                    "course": random.randint(100, 199),  # ID курсов
                    "user": random.randint(100, 169),    # ID пользователей
                    "rating": random.randint(3, 5),
                    "text": f"Отзыв о курсе {i}",
                    "created_at": timezone.now().isoformat(),
                    "updated_at": timezone.now().isoformat()
                }
            }
            reviews.append(review)
        return reviews

    def generate_enrollments(self, num_enrollments=300):
        enrollments = []
        statuses = ["active", "completed", "dropped"]
        for i in range(num_enrollments):
            status = random.choice(statuses)
            enrollment = {
                "model": "courses.enrollment",
                "pk": i + 100,
                "fields": {
                    "student": random.randint(100, 169),  # ID студентов
                    "course": random.randint(100, 199),   # ID курсов
                    "enrolled_at": timezone.now().isoformat(),
                    "status": status,
                    "completed_at": timezone.now().isoformat() if status == "completed" else None,
                    "progress": random.randint(0, 100),
                    "last_accessed": timezone.now().isoformat()
                }
            }
            enrollments.append(enrollment)
        return enrollments

    @staticmethod
    def slugify_ru(text):
        """Простая транслитерация для русских слов"""
        ru_en = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
            'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        text = text.lower()
        slug = ''
        for char in text:
            slug += ru_en.get(char, char)
        return slug.replace(' ', '-')

    def handle(self, *args, **options):
        # Сначала генерируем базовые сущности
        data = []
        
        # Генерируем данные в правильном порядке
        data.extend(self.generate_users(100))  # 70 студентов, 20 учителей, 10 продюсеров
        data.extend(self.generate_specializations(20))
        data.extend(self.generate_student_profiles(70))  # Профили для студентов
        data.extend(self.generate_teacher_profiles(20))  # Профили для учителей
        data.extend(self.generate_producer_profiles(10))  # Профили для продюсеров
        data.extend(self.generate_courses(100))
        data.extend(self.generate_modules(300))
        data.extend(self.generate_lessons(1000))
        data.extend(self.generate_reviews(500))
        data.extend(self.generate_enrollments(300))

        # Сохраняем в файл
        output_file = 'demo/fixtures/generated_demo_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Сгенерировано {len(data)} записей'))
