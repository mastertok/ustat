from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import ProducerProfile, TeacherProfile, Specialization
from courses.models import Category, Tag, Course, Module, Lesson
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Loads demo data into the database'

    def generate_teachers(self):
        first_names_male = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артём", "Илья", "Кирилл", "Михаил",
                          "Никита", "Матвей", "Роман", "Егор", "Арсен", "Владимир", "Ярослав", "Тимур", "Павел", "Богдан"]
        first_names_female = ["Анна", "Мария", "Елена", "Дарья", "София", "Алиса", "Виктория", "Полина", "Екатерина", "Ксения",
                           "Валерия", "Юлия", "Татьяна", "Наталья", "Ольга", "Светлана", "Алина", "Ирина", "Марина", "Евгения"]
        last_names_male = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов", "Михайлов", "Новиков", "Федоров",
                         "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев"]
        last_names_female = ["Иванова", "Смирнова", "Кузнецова", "Попова", "Васильева", "Петрова", "Соколова", "Михайлова", "Новикова", "Федорова",
                          "Морозова", "Волкова", "Алексеева", "Лебедева", "Семенова", "Егорова", "Павлова", "Козлова", "Степанова", "Николаева"]
        
        specializations = ["Математика", "Физика", "Информатика", "Английский язык", "Русский язык", 
                         "История", "Биология", "Химия", "География", "Литература"]
        universities = ["МГУ", "КГТУ", "КНУ", "КРСУ", "АУЦА", "КГМА", "НГУ", "СПбГУ", "ТомГУ", "НГУ"]
        faculties = ["Факультет математики", "Факультет физики", "Факультет информатики", 
                    "Факультет филологии", "Факультет истории", "Факультет биологии"]

        teachers = []
        for i in range(35):
            is_male = random.choice([True, False])
            first_name = random.choice(first_names_male if is_male else first_names_female)
            last_name = random.choice(last_names_male if is_male else last_names_female)
            
            user = User.objects.create_user(
                username=f"teacher{i+1}",
                email=f"teacher{i+1}@example.com",
                password=f"teacher{i+1}pass",
                first_name=first_name,
                last_name=last_name,
                role='teacher',
                bio=f"Преподаватель с опытом работы {random.randint(3, 20)} лет",
                phone=f"+99670{random.randint(1000000, 9999999)}"
            )

            specialization = random.choice(specializations)
            spec_obj, _ = Specialization.objects.get_or_create(
                name=specialization,
                slug=specialization.lower().replace(' ', '-'),
                description=f"Специализация в области {specialization.lower()}"
            )

            teacher_profile = TeacherProfile.objects.create(
                user=user,
                experience_summary=f"Опытный преподаватель {specialization}",
                education_summary=f"{random.choice(universities)}, {random.choice(faculties)}",
                teaching_style=f"Индивидуальный подход к каждому ученику",
                slug=f"teacher-{i+1}"
            )
            teacher_profile.specializations.add(spec_obj)
            teachers.append(teacher_profile)
        
        return teachers

    def generate_courses(self, teachers):
        categories = [
            {"name": "Математика", "slug": "mathematics", "description": "Курсы по математике всех уровней"},
            {"name": "Физика", "slug": "physics", "description": "Курсы по физике"},
            {"name": "Информатика", "slug": "informatics", "description": "Курсы по информатике и программированию"},
            {"name": "Английский язык", "slug": "english", "description": "Курсы английского языка"},
            {"name": "Русский язык", "slug": "russian", "description": "Курсы русского языка"},
            {"name": "История", "slug": "history", "description": "Исторические курсы"},
            {"name": "Биология", "slug": "biology", "description": "Курсы по биологии"},
            {"name": "Химия", "slug": "chemistry", "description": "Курсы по химии"},
            {"name": "География", "slug": "geography", "description": "Курсы по географии"},
            {"name": "Литература", "slug": "literature", "description": "Курсы по литературе"}
        ]

        tags = [
            {"name": "Для начинающих", "slug": "for-beginners"},
            {"name": "Продвинутый уровень", "slug": "advanced"},
            {"name": "Практические занятия", "slug": "practice"},
            {"name": "Теория", "slug": "theory"},
            {"name": "Подготовка к экзаменам", "slug": "exam-prep"},
            {"name": "Интенсив", "slug": "intensive"},
            {"name": "Для детей", "slug": "for-kids"},
            {"name": "Для взрослых", "slug": "for-adults"},
            {"name": "Онлайн обучение", "slug": "online"},
            {"name": "Видеоуроки", "slug": "video-lessons"}
        ]

        # Создаем категории
        category_objects = []
        for cat in categories:
            category_obj, _ = Category.objects.get_or_create(
                name=cat["name"],
                defaults={
                    "slug": cat["slug"],
                    "description": cat["description"]
                }
            )
            category_objects.append(category_obj)

        # Создаем теги
        tag_objects = []
        for tag in tags:
            tag_obj, _ = Tag.objects.get_or_create(
                name=tag["name"],
                defaults={
                    "slug": tag["slug"]
                }
            )
            tag_objects.append(tag_obj)

        # Создаем курсы
        course_titles = {
            "Математика": [
                "Алгебра для начинающих", "Геометрия базовый курс", "Высшая математика",
                "Математический анализ", "Тригонометрия", "Теория вероятностей"
            ],
            "Физика": [
                "Механика", "Электричество и магнетизм", "Оптика", "Квантовая физика",
                "Термодинамика", "Астрофизика"
            ],
            "Информатика": [
                "Python для начинающих", "Java базовый курс", "Web-разработка",
                "Основы программирования", "Базы данных", "Алгоритмы и структуры данных"
            ],
            "Английский язык": [
                "English for Beginners", "Business English", "IELTS Preparation",
                "English Grammar", "Speaking Club", "Academic Writing"
            ]
        }

        difficulty_levels = ["beginner", "intermediate", "advanced"]
        languages = ["ru", "ky", "en"]
        course_types = ["free", "paid"]

        for i in range(50):
            category = random.choice(category_objects)
            teacher = random.choice(teachers)
            course_title = random.choice(course_titles.get(category.name, course_titles["Математика"]))
            course_slug = f"{course_title.lower().replace(' ', '-')}-{i+1}"

            course = Course.objects.create(
                title=f"{course_title} #{i+1}",
                slug=course_slug,
                description=f"<p>Подробное описание курса {course_title}</p>",
                excerpt=f"Краткое описание курса {course_title}",
                category=category,
                teacher=teacher,
                producer=ProducerProfile.objects.first(),
                max_students=random.randint(20, 100),
                difficulty_level=random.choice(difficulty_levels),
                language=random.choice(languages),
                duration_minutes=random.randint(600, 4800),
                enable_qa=True,
                enable_announcements=True,
                enable_reviews=True,
                course_type=random.choice(course_types),
                price=str(random.randint(3000, 15000)) + ".00",
                currency="KGS",
                status="published",
                seo_title=f"{course_title} - Онлайн курс",
                seo_description=f"Изучите {course_title.lower()} онлайн",
                seo_keywords=f"{course_title.lower()}, обучение, онлайн курс",
                published_at=timezone.now()
            )

            # Добавляем случайные теги
            course.tags.add(*random.sample(tag_objects, k=random.randint(2, 5)))

            # Создаем модули для курса
            num_modules = random.randint(3, 7)
            for j in range(num_modules):
                module = Module.objects.create(
                    course=course,
                    title=f"Модуль {j+1}: {random.choice(['Введение', 'Основы', 'Практика', 'Теория', 'Продвинутые темы'])}",
                    description=f"Описание модуля {j+1}",
                    order=j+1
                )

                # Создаем уроки для модуля
                num_lessons = random.randint(3, 7)
                for k in range(num_lessons):
                    Lesson.objects.create(
                        module=module,
                        title=f"Урок {k+1}: {random.choice(['Теория', 'Практика', 'Тест', 'Задачи'])}",
                        content_type=random.choice(['video', 'text', 'test', 'presentation']),
                        content=f"<p>Содержание урока {k+1}</p>",
                        order=k+1,
                        duration_minutes=random.randint(30, 90)
                    )

    def handle(self, *args, **options):
        try:
            # Создаем продюсера
            producer_user = User.objects.create_user(
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
                user=producer_user,
                company='Education Production'
            )

            # Генерируем учителей
            teachers = self.generate_teachers()

            # Генерируем курсы
            self.generate_courses(teachers)

            self.stdout.write(self.style.SUCCESS('Successfully loaded demo data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading demo data: {str(e)}'))
