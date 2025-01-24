from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models import Avg, Count
from django.utils import timezone
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models
from core.models import BaseModel

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
)

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
    
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='student', db_index=True)
    bio = models.TextField('Биография', blank=True)
    avatar = models.ImageField('Фото профиля', upload_to='avatars/', blank=True)
    phone = models.CharField(
        'Телефон',
        max_length=15,
        blank=True,
        unique=True,
        validators=[phone_regex]
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['role', 'username']),
            models.Index(fields=['role', 'email']),
            models.Index(fields=['role', 'username'], condition=models.Q(is_active=True), name='active_users_idx'),
            models.Index(fields=['date_joined', 'role']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(role__in=['student', 'teacher', 'producer', 'admin']),
                name='valid_role'
            )
        ]
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
        ]

    def get_role_permissions(self):
        """Возвращает список разрешений в зависимости от роли пользователя"""
        permissions = []
        if self.is_student():
            permissions.extend(['can_enroll_course', 'can_view_course_content', 'can_leave_review'])
        elif self.is_teacher():
            permissions.extend(['can_create_course', 'can_edit_own_course', 'can_view_course_analytics'])
        elif self.is_producer():
            permissions.extend(['can_edit_course_landing', 'can_manage_promotions', 'can_view_marketing_analytics'])
        return permissions

    def has_role_permission(self, permission):
        """Проверяет, есть ли у пользователя разрешение в соответствии с его ролью"""
        return permission in self.get_role_permissions()

    def is_student(self):
        return self.role == 'student'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_producer(self):
        return self.role == 'producer'

    def get_absolute_url(self):
        return reverse('accounts:user_profile', kwargs={'username': self.username})

class Profile(BaseModel):
    """
    Профиль пользователя с дополнительной информацией
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rating = models.DecimalField(
        'Рейтинг',
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    social_links = models.JSONField('Социальные сети', default=dict, blank=True)
    slug = models.SlugField('URL', max_length=150, unique=True)
    specializations = models.ManyToManyField(
        'Specialization',
        verbose_name='Специализации',
        related_name='profiles',
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        indexes = [
            models.Index(fields=['user', 'rating']),
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'slug': self.slug})

    def get_rating(self):
        """Вычисляет средний рейтинг на основе отзывов о курсах"""
        if hasattr(self.user, 'courses'):
            return self.user.courses.aggregate(
                avg_rating=Avg('reviews__rating')
            )['avg_rating'] or 0.0
        return 0.0

    def update_rating(self):
        """Обновляет рейтинг профиля"""
        self.rating = self.get_rating()
        self.save(update_fields=['rating'])

class RoleSpecificData(BaseModel):
    """
    Модель для хранения специфичных данных каждой роли
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='role_specific_data')
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    data = models.JSONField('Данные')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Данные роли'
        verbose_name_plural = 'Данные ролей'
        unique_together = ['profile', 'role']
        indexes = [
            models.Index(fields=['profile', 'role']),
            models.Index(fields=['-updated_at']),
        ]

class AuditLog(BaseModel):
    """
    Модель для аудита действий пользователей
    """
    ACTION_CHOICES = (
        ('create', 'Создание'),
        ('update', 'Изменение'),
        ('delete', 'Удаление'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(contenttypes_models.ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = contenttypes_fields.GenericForeignKey('content_type', 'object_id')
    changes = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Лог аудита'
        verbose_name_plural = 'Логи аудита'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} - {self.content_type} - {self.timestamp}"

class Specialization(BaseModel):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    slug = models.CharField('URL', max_length=150, unique=True)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Education(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education_records')
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
        indexes = [
            models.Index(fields=['profile', 'start_date']),
            models.Index(fields=['profile', 'end_date']),
        ]

    def __str__(self):
        return f"{self.degree} в {self.institution}"

class WorkExperience(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experiences')
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
        indexes = [
            models.Index(fields=['profile', 'is_current']),
            models.Index(fields=['profile', 'start_date']),
        ]

    def __str__(self):
        return f"{self.position} в {self.company}"

    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)

class Achievement(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='achievement_records')
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
        indexes = [
            models.Index(fields=['profile', 'date_received']),
        ]

    def __str__(self):
        return f"{self.title} от {self.issuer}"
