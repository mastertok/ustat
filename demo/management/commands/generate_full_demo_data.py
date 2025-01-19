from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.text import slugify
from accounts.models import User, TeacherProfile, ProducerProfile, Education, WorkExperience, Achievement, Specialization
from courses.models import Course, Category, Tag, Module, Lesson, Review, Enrollment, Promocode, Promotion
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Генерирует полный набор демо-данных'

    def handle(self, *args, **options):
        self.stdout.write('Генерация демо-данных...')
        
        # Создаем категории
        categories = self._create_categories()
        
        # Создаем теги
        tags = self._create_tags()
        
        # Создаем учителей
        teachers = self._create_teachers()
        
        # Создаем продюсеров
        producers = self._create_producers()
        
        # Создаем студентов
        students = self._create_students()
        
        # Создаем курсы
        courses = self._create_courses(teachers, categories, tags)
        
        # Создаем записи на курсы
        self._create_enrollments(students, courses)
        
        # Создаем отзывы
        self._create_reviews(students, courses)
        
        # Создаем промокоды и акции
        self._create_promotions(producers, courses)
        
        self.stdout.write(self.style.SUCCESS('Демо-данные успешно созданы!'))

    def _create_categories(self):
        categories_data = [
            ('Математика', 'mathematics'),
            ('Английский язык', 'english'),
            ('Программирование', 'programming'),
            ('Физика', 'physics'),
            ('Химия', 'chemistry'),
            ('Биология', 'biology'),
            ('История', 'history'),
            ('География', 'geography'),
            ('Литература', 'literature'),
            ('Искусство', 'art')
        ]
        
        categories = []
        for name, slug in categories_data:
            cat = Category.objects.create(
                name=name,
                slug=slug,
                description=f'Курсы по предмету {name}'
            )
            categories.append(cat)
        
        return categories

    def _create_tags(self):
        tags_data = [
            ('ОРТ', 'ort'),
            ('IELTS', 'ielts'),
            ('Для начинающих', 'for-beginners'),
            ('Продвинутый уровень', 'advanced'),
            ('Интенсив', 'intensive'),
            ('Онлайн', 'online'),
            ('С нуля', 'from-scratch'),
            ('Для детей', 'for-kids'),
            ('Для взрослых', 'for-adults'),
            ('Подготовка к экзаменам', 'exam-prep')
        ]
        
        tags = []
        for name, slug in tags_data:
            tag = Tag.objects.create(name=name, slug=slug)
            tags.append(tag)
        
        return tags

    def _create_teachers(self):
        teachers_data = [
            ('Айгуль', 'Асанова', 'Математика'),
            ('Бакыт', 'Эшматов', 'Английский язык'),
            ('Чынара', 'Жумабаева', 'Программирование'),
            ('Данияр', 'Алиев', 'Физика'),
            ('Елена', 'Ким', 'Химия'),
            ('Фарида', 'Бакирова', 'Биология'),
            ('Гульнара', 'Сыдыкова', 'История'),
            ('Хасан', 'Мамытов', 'География'),
            ('Ирина', 'Петрова', 'Литература'),
            ('Жамал', 'Алымкулова', 'Искусство'),
            ('Марат', 'Джумаев', 'Математика'),
            ('Наталья', 'Ким', 'Английский язык'),
            ('Олег', 'Попов', 'Программирование'),
            ('Павел', 'Иванов', 'Физика'),
            ('Рахат', 'Асанов', 'Химия'),
            ('Салтанат', 'Омурова', 'Биология'),
            ('Тимур', 'Ахметов', 'История'),
            ('Умут', 'Касымова', 'География'),
            ('Феруза', 'Хасанова', 'Литература'),
            ('Эльмира', 'Садырова', 'Искусство')
        ]
        
        teachers = []
        for first_name, last_name, subject in teachers_data:
            username = f"{slugify(first_name)}.{slugify(last_name)}"
            user = User.objects.create(
                username=username,
                email=f"{username}@example.com",
                password=make_password('teacher12345'),
                first_name=first_name,
                last_name=last_name,
                role='teacher',
                is_active=True,
                bio=f"Опытный преподаватель {subject.lower()}",
                phone=f"+99670{random.randint(1000000, 9999999)}"
            )
            
            profile = TeacherProfile.objects.create(
                user=user,
                experience_summary=f"{random.randint(5, 20)} лет преподавания {subject.lower()}",
                achievements_summary="Победитель профессиональных конкурсов",
                education_summary="Высшее педагогическое образование",
                rating=round(random.uniform(4.0, 5.0), 2),
                students_count=random.randint(50, 300),
                reviews_count=random.randint(10, 50),
                teaching_style="Индивидуальный подход к каждому ученику",
                slug=username
            )
            
            # Добавляем образование
            Education.objects.create(
                teacher=profile,
                institution="КНУ им. Ж.Баласагына",
                degree="Магистр",
                field_of_study=subject,
                start_date=timezone.now() - timedelta(days=random.randint(3650, 7300)),
                end_date=timezone.now() - timedelta(days=random.randint(1825, 3649))
            )
            
            # Добавляем опыт работы
            WorkExperience.objects.create(
                teacher=profile,
                company="Школа №61",
                position=f"Учитель {subject.lower()}",
                start_date=timezone.now() - timedelta(days=random.randint(1825, 3649)),
                is_current=True,
                description=f"Преподавание {subject.lower()} в старших классах"
            )
            
            # Добавляем достижения
            Achievement.objects.create(
                teacher=profile,
                title="Учитель года",
                date_received=timezone.now() - timedelta(days=random.randint(0, 365)),
                issuer="Министерство образования КР",
                description="Победитель республиканского конкурса"
            )
            
            teachers.append(user)
        
        return teachers

    def _create_producers(self):
        producers_data = [
            ('Азамат', 'Касымов', 'Digital Education KG'),
            ('Бектур', 'Исаев', 'Online Academy'),
            ('Венера', 'Турсунова', 'Smart Learning'),
            ('Гульзат', 'Мамытова', 'Future Skills'),
            ('Джамиля', 'Асанова', 'Education Plus'),
            ('Ержан', 'Кулов', 'Knowledge Hub'),
            ('Жылдыз', 'Бакирова', 'Study Center'),
            ('Замир', 'Орозов', 'Learning Lab'),
            ('Ильяс', 'Ахметов', 'Skills Box'),
            ('Камила', 'Сыдыкова', 'Education Pro'),
            ('Лариса', 'Ким', 'Study Max'),
            ('Мирлан', 'Джумаев', 'Knowledge Base'),
            ('Нургуль', 'Алиева', 'Learning Point'),
            ('Омурбек', 'Касымов', 'Skills Pro'),
            ('Перизат', 'Бакирова', 'Education Max'),
            ('Руслан', 'Асанов', 'Study Lab'),
            ('Саида', 'Омурова', 'Learning Box'),
            ('Таалай', 'Ахметов', 'Skills Hub'),
            ('Уулжан', 'Касымова', 'Education Lab'),
            ('Чолпон', 'Садырова', 'Knowledge Pro')
        ]
        
        producers = []
        for first_name, last_name, company in producers_data:
            username = f"{slugify(first_name)}.{slugify(last_name)}"
            user = User.objects.create(
                username=username,
                email=f"{username}@example.com",
                password=make_password('producer12345'),
                first_name=first_name,
                last_name=last_name,
                role='producer',
                is_active=True,
                bio=f"Продюсер онлайн-курсов, {company}",
                phone=f"+99670{random.randint(1000000, 9999999)}"
            )
            
            ProducerProfile.objects.create(
                user=user,
                company=company,
                portfolio=f"https://portfolio.example.com/{username}"
            )
            
            producers.append(user)
        
        return producers

    def _create_students(self):
        students_data = [
            ('Алтынай', 'Асанова'),
            ('Бермет', 'Алиева'),
            ('Василий', 'Ким'),
            ('Гулжан', 'Омурова'),
            ('Дастан', 'Касымов'),
            ('Елена', 'Попова'),
            ('Жаркын', 'Бакиров'),
            ('Зарина', 'Ахметова'),
            ('Ильгиз', 'Алиев'),
            ('Канат', 'Джумаев'),
            ('Лейла', 'Сыдыкова'),
            ('Максат', 'Орозов'),
            ('Нурзат', 'Бакирова'),
            ('Омурбек', 'Асанов'),
            ('Перизат', 'Касымова'),
            ('Расул', 'Ахметов'),
            ('Салтанат', 'Алиева'),
            ('Тимур', 'Попов'),
            ('Улан', 'Бакиров'),
            ('Фатима', 'Омурова')
        ]
        
        students = []
        for first_name, last_name in students_data:
            username = f"{slugify(first_name)}.{slugify(last_name)}"
            user = User.objects.create(
                username=username,
                email=f"{username}@example.com",
                password=make_password('student12345'),
                first_name=first_name,
                last_name=last_name,
                role='student',
                is_active=True,
                bio=f"Студент, изучаю онлайн-курсы",
                phone=f"+99670{random.randint(1000000, 9999999)}"
            )
            students.append(user)
        
        return students

    def _create_courses(self, teachers, categories, tags):
        courses_data = [
            ('Подготовка к ОРТ по математике', 'mathematics', 5000),
            ('IELTS Academic Preparation', 'english', 6000),
            ('Python для начинающих', 'programming', 4500),
            ('Подготовка к олимпиаде по физике', 'physics', 5500),
            ('Органическая химия', 'chemistry', 5000),
            ('Биология для ОРТ', 'biology', 4800),
            ('История Кыргызстана', 'history', 4000),
            ('География мира', 'geography', 4200),
            ('Русская литература', 'literature', 4500),
            ('Живопись для начинающих', 'art', 3500),
            ('Высшая математика', 'mathematics', 6500),
            ('TOEFL Preparation', 'english', 7000),
            ('Java Programming', 'programming', 5500),
            ('Квантовая физика', 'physics', 6000),
            ('Неорганическая химия', 'chemistry', 5200),
            ('Анатомия человека', 'biology', 5500),
            ('Мировая история', 'history', 4800),
            ('Экономическая география', 'geography', 4500),
            ('Кыргызская литература', 'literature', 4000),
            ('Скульптура', 'art', 4500)
        ]
        
        courses = []
        for i, (title, category_slug, price) in enumerate(courses_data):
            teacher = teachers[i % len(teachers)]
            category = Category.objects.get(slug=category_slug)
            
            course = Course.objects.create(
                title=title,
                slug=slugify(title),
                teacher=teacher,
                category=category,
                description=f"Полный курс {title.lower()}",
                price=price,
                difficulty_level=random.choice(['beginner', 'intermediate', 'advanced']),
                language=random.choice(['kyrgyz', 'russian', 'english']),
                duration_weeks=random.randint(8, 16),
                total_duration_hours=random.randint(24, 48),
                rating=round(random.uniform(4.0, 5.0), 2),
                students_count=random.randint(20, 100),
                reviews_count=random.randint(5, 30),
                is_published=True
            )
            
            # Создаем модули
            for j in range(1, random.randint(4, 8)):
                module = Module.objects.create(
                    course=course,
                    title=f"Модуль {j}",
                    description=f"Описание модуля {j}",
                    order=j
                )
                
                # Создаем уроки
                for k in range(1, random.randint(3, 6)):
                    Lesson.objects.create(
                        module=module,
                        title=f"Урок {k}",
                        content_type=random.choice(['video', 'text', 'test', 'presentation']),
                        content=f"Содержание урока {k}",
                        video_url="https://youtube.com/watch?v=example" if random.choice([True, False]) else None,
                        duration_minutes=random.randint(30, 90),
                        order=k
                    )
            
            courses.append(course)
        
        return courses

    def _create_enrollments(self, students, courses):
        for student in students:
            # Каждый студент записывается на 2-5 случайных курсов
            for course in random.sample(courses, random.randint(2, 5)):
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    status=random.choice(['active', 'completed', 'dropped']),
                    progress=random.randint(0, 100),
                    last_accessed=timezone.now() - timedelta(days=random.randint(0, 30))
                )

    def _create_reviews(self, students, courses):
        for student in students:
            # Каждый студент оставляет отзывы на 1-3 курса
            for course in random.sample(courses, random.randint(1, 3)):
                Review.objects.create(
                    course=course,
                    user=student,
                    rating=random.randint(3, 5),
                    text=f"Отличный курс! Очень доволен обучением.",
                    created_at=timezone.now() - timedelta(days=random.randint(0, 30))
                )

    def _create_promotions(self, producers, courses):
        for producer in producers[:5]:  # Создаем промокоды только для первых 5 продюсеров
            producer_profile = producer.producer_profile
            
            # Создаем промокод
            promocode = Promocode.objects.create(
                code=f"PROMO{random.randint(1000, 9999)}",
                discount_percent=random.randint(10, 30),
                valid_from=timezone.now(),
                valid_until=timezone.now() + timedelta(days=30),
                max_uses=100,
                used_count=random.randint(0, 50),
                created_by=producer_profile
            )
            
            # Добавляем случайные курсы к промокоду
            promocode.courses.set(random.sample(courses, random.randint(3, 7)))
            
            # Создаем акцию
            promotion = Promotion.objects.create(
                title=f"Акция от {producer.first_name}",
                description="Специальное предложение на курсы",
                discount_percent=random.randint(20, 40),
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=14),
                created_by=producer_profile
            )
            
            # Добавляем случайные курсы к акции
            promotion.courses.set(random.sample(courses, random.randint(3, 7)))
