from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Avg, Count
from core.models import AutoRegisterAdmin
from django.utils import timezone

class User(AbstractUser):
    """
    Расширенная модель пользователя с различными ролями и их возможностями
    """
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Учитель'),
        ('producer', 'Продюсер'),
        ('admin', 'Администратор'),
    )
    
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField('Биография', blank=True)
    avatar = models.ImageField('Фото профиля', upload_to='avatars/', blank=True)
    phone = models.CharField('Телефон', max_length=15, blank=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            # Права для студента
            ("can_enroll_course", "Может записаться на курс"),
            ("can_view_course_content", "Может просматривать содержимое курса"),
            ("can_leave_review", "Может оставлять отзывы"),
            
            # Права для учителя
            ("can_create_course", "Может создавать курсы"),
            ("can_edit_own_course", "Может редактировать свои курсы"),
            ("can_view_course_analytics", "Может просматривать аналитику своих курсов"),
            ("can_interact_with_students", "Может взаимодействовать со студентами"),
            
            # Права для продюсера
            ("can_edit_course_landing", "Может редактировать лендинги курсов"),
            ("can_manage_promotions", "Может управлять акциями и промокодами"),
            ("can_view_marketing_analytics", "Может просматривать маркетинговую аналитику"),
            ("can_manage_advertising", "Может управлять рекламой"),
            ("can_manage_email_campaigns", "Может управлять email-рассылками"),
            
            # Права для администратора
            ("can_manage_users", "Может управлять пользователями"),
            ("can_manage_all_courses", "Может управлять всеми курсами"),
            ("can_manage_site_settings", "Может управлять настройками сайта"),
        ]

    def get_role_permissions(self):
        """Возвращает список разрешений в зависимости от роли пользователя"""
        permissions = {
            'student': [
                'can_enroll_course',
                'can_view_course_content',
                'can_leave_review',
            ],
            'teacher': [
                'can_create_course',
                'can_edit_own_course',
                'can_view_course_analytics',
                'can_interact_with_students',
            ],
            'producer': [
                'can_edit_course_landing',
                'can_manage_promotions',
                'can_view_marketing_analytics',
                'can_manage_advertising',
                'can_manage_email_campaigns',
            ],
            'admin': [
                'can_manage_users',
                'can_manage_all_courses',
                'can_manage_site_settings',
            ],
        }
        return permissions.get(self.role, [])

    def has_role_permission(self, permission):
        """Проверяет, есть ли у пользователя разрешение в соответствии с его ролью"""
        return permission in self.get_role_permissions()

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_producer(self):
        return self.role == 'producer'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def get_absolute_url(self):
        if self.is_teacher:
            return reverse('accounts:teacher_profile', kwargs={'slug': self.teacher_profile.slug})
        return reverse('accounts:user_profile', kwargs={'username': self.username})

class Specialization(AutoRegisterAdmin):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Education(AutoRegisterAdmin):
    teacher = models.ForeignKey('TeacherProfile', on_delete=models.CASCADE, related_name='education_records')
    institution = models.CharField('Учебное заведение', max_length=200)
    degree = models.CharField('Степень/Квалификация', max_length=100)
    field_of_study = models.CharField('Направление обучения', max_length=100)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'
        ordering = ['-end_date', '-start_date']

    def __str__(self):
        return f"{self.degree} - {self.institution}"

class WorkExperience(AutoRegisterAdmin):
    teacher = models.ForeignKey('TeacherProfile', on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField('Компания/Организация', max_length=200)
    position = models.CharField('Должность', max_length=100)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    description = models.TextField('Описание обязанностей', blank=True)
    is_current = models.BooleanField('Текущее место работы', default=False)

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.position} в {self.company}"

    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)

class Achievement(AutoRegisterAdmin):
    teacher = models.ForeignKey('TeacherProfile', on_delete=models.CASCADE, related_name='achievement_records')
    title = models.CharField('Название', max_length=200)
    date_received = models.DateField('Дата получения')
    issuer = models.CharField('Кем выдано', max_length=200)
    description = models.TextField('Описание', blank=True)
    certificate_file = models.FileField('Файл сертификата', upload_to='certificates/', blank=True)
    certificate_link = models.URLField('Ссылка на сертификат', blank=True)
    
    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-date_received']

    def __str__(self):
        return self.title

class TeacherProfile(AutoRegisterAdmin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    specializations = models.ManyToManyField(Specialization, verbose_name='Специализации', related_name='teachers')
    experience_summary = models.TextField('Краткое описание опыта', blank=True)
    achievements_summary = models.TextField('Краткое описание достижений', blank=True)
    education_summary = models.TextField('Краткое описание образования', blank=True)
    rating = models.DecimalField('Рейтинг', max_digits=3, decimal_places=2, default=0)
    students_count = models.PositiveIntegerField('Количество учеников', default=0)
    reviews_count = models.PositiveIntegerField('Количество отзывов', default=0)
    social_links = models.JSONField('Социальные сети', default=dict, blank=True)
    teaching_style = models.TextField('Стиль преподавания', blank=True)
    slug = models.SlugField('URL', unique=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Профиль учителя'
        verbose_name_plural = 'Профили учителей'

    def __str__(self):
        return f"{self.user.get_full_name()}"

    def total_experience_years(self):
        """Подсчитывает общий опыт работы в годах"""
        total_years = 0
        for exp in self.work_experiences.all():
            end_date = exp.end_date or timezone.now().date()
            years = (end_date - exp.start_date).days / 365
            total_years += years
        return round(total_years, 1)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.get_full_name()}-{self.user.username}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('teacher_profile_detail', kwargs={'slug': self.slug})

    def update_rating(self):
        """Обновляет рейтинг учителя на основе отзывов всех его курсов"""
        from courses.models import Course, Review
        courses = Course.objects.filter(teacher=self)
        avg_rating = Review.objects.filter(course__in=courses).aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            self.rating = round(avg_rating, 2)
            self.save(update_fields=['rating'])

    def update_reviews_count(self):
        """Обновляет количество отзывов для всех курсов учителя"""
        from courses.models import Course, Review
        courses = Course.objects.filter(teacher=self)
        self.reviews_count = Review.objects.filter(course__in=courses).count()
        self.save(update_fields=['reviews_count'])

    def update_students_count(self):
        """Обновляет количество уникальных студентов на всех курсах учителя"""
        from courses.models import Course, Enrollment
        courses = Course.objects.filter(teacher=self)
        self.students_count = Enrollment.objects.filter(course__in=courses).values('student').distinct().count()
        self.save(update_fields=['students_count'])

    def total_courses(self):
        """Возвращает общее количество курсов учителя"""
        from courses.models import Course
        return Course.objects.filter(teacher=self).count()

    def published_courses(self):
        """Возвращает количество опубликованных курсов учителя"""
        from courses.models import Course
        return Course.objects.filter(teacher=self, status='published').count()

class StudentProfile(AutoRegisterAdmin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    interests = models.TextField('Интересы', blank=True)
    education_level = models.CharField('Уровень образования', max_length=20, choices=[
        ('school', 'Школьник'),
        ('bachelor', 'Бакалавр'),
        ('master', 'Магистр'),
        ('phd', 'PhD')
    ])
    
    class Meta:
        verbose_name = 'Профиль студента'
        verbose_name_plural = 'Профили студентов'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_education_level_display()}"

class ProducerProfile(AutoRegisterAdmin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='producer_profile')
    company = models.CharField('Компания', max_length=100, blank=True)
    portfolio = models.URLField('Портфолио', blank=True)
    
    class Meta:
        verbose_name = 'Профиль продюсера'
        verbose_name_plural = 'Профили продюсеров'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company if self.company else 'Независимый продюсер'}"
