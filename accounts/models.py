from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('producer', 'Продюсер'),
        ('partner', 'Партнер'),
        ('editor', 'Редактор'),
    )

    username = None
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=15, blank=True)
    role = models.CharField('Роль', max_length=20, choices=ROLES, default='student')
    is_verified = models.BooleanField('Верифицирован', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['email', 'role']),
            models.Index(fields=['is_verified', 'role']),
        ]

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField('Фото', upload_to='avatars/', null=True, blank=True)
    bio = models.TextField('Биография', blank=True)
    language = models.CharField('Язык', max_length=10, blank=True)
    social_links = models.JSONField('Социальные сети', default=dict, blank=True)
    role_data = models.JSONField('Данные роли', default=dict, blank=True)
    custom_url = models.SlugField('URL профиля', max_length=100, unique=True, blank=True, null=True)
    rating = models.DecimalField(
        'Рейтинг',
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    courses_count = models.PositiveIntegerField('Количество курсов', default=0)
    reviews_count = models.PositiveIntegerField('Количество отзывов', default=0)
    verification_status = models.CharField('Статус верификации', max_length=20, default='pending')
    verified_at = models.DateTimeField('Дата верификации', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        indexes = [
            models.Index(fields=['user', 'verification_status']),
            models.Index(fields=['rating', '-courses_count']),
            models.Index(fields=['custom_url']),
        ]

    def __str__(self):
        return f'Профиль {self.user.email}'

    def save(self, *args, **kwargs):
        if self.user.role == 'teacher' and not self.custom_url:
            self.generate_custom_url()
        super().save(*args, **kwargs)

    def generate_custom_url(self):
        """Генерирует уникальный URL для профиля преподавателя"""
        base = slugify(f"{self.user.first_name} {self.user.last_name}")
        if not base:
            base = slugify(self.user.email.split('@')[0])
        
        url = base
        counter = 1
        while Profile.objects.filter(custom_url=url).exists():
            url = f"{base}-{counter}"
            counter += 1
        
        self.custom_url = url

    def get_absolute_url(self):
        """Возвращает URL профиля"""
        if self.user.role == 'teacher' and self.custom_url:
            return reverse('teacher:profile', kwargs={'custom_url': self.custom_url})
        return reverse('profile', kwargs={'pk': self.pk})

    def get_courses_url(self):
        """Возвращает URL списка курсов преподавателя"""
        if self.user.role == 'teacher' and self.custom_url:
            return reverse('teacher:courses', kwargs={'custom_url': self.custom_url})
        return None

    def get_role_specific_data(self):
        """Получение данных, специфичных для роли пользователя"""
        return self.role_data.get(self.user.role, {})

    def update_role_data(self, data):
        """Обновление данных, специфичных для роли"""
        current_data = self.role_data
        current_data[self.user.role] = data
        self.role_data = current_data
        self.save()

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField('Учебное заведение', max_length=200)
    degree = models.CharField('Степень', max_length=100)
    field_of_study = models.CharField('Область изучения', max_length=200)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образования'
        ordering = ['-end_date', '-start_date']

    def __str__(self):
        return f"{self.degree} в {self.institution}"

class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experience')
    company = models.CharField('Компания', max_length=200)
    position = models.CharField('Должность', max_length=200)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыты работы'
        ordering = ['-end_date', '-start_date']

    def __str__(self):
        return f"{self.position} в {self.company}"

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    date = models.DateField('Дата получения')
    certificate = models.FileField('Сертификат', upload_to='certificates/', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-date']

    def __str__(self):
        return self.title
