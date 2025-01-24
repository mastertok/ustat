from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.core.cache import cache
from ckeditor.fields import RichTextField
from accounts.models import User
from core.models import BaseModel

def validate_video_url(value):
    """Валидация URL видео (YouTube, Vimeo)"""
    if not any(platform in value.lower() for platform in ['youtube.com', 'youtu.be', 'vimeo.com']):
        raise ValidationError('URL должен быть с YouTube или Vimeo')

def validate_image_size(value):
    """Валидация размера изображения (макс. 2MB)"""
    if value.size > 2 * 1024 * 1024:
        raise ValidationError('Максимальный размер изображения 2MB')

class Category(BaseModel):
    name = models.CharField('Название', max_length=100, db_index=True)
    slug = models.SlugField('URL', unique=True, db_index=True)
    description = models.TextField('Описание', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='Родительская категория')
    
    # Вычисляемые поля
    courses_count = models.PositiveIntegerField('Количество курсов', default=0)
    active_courses_count = models.PositiveIntegerField('Активные курсы', default=0)
    total_students = models.PositiveIntegerField('Всего студентов', default=0)
    average_course_rating = models.DecimalField('Средний рейтинг курсов', 
                                              max_digits=3, decimal_places=2, default=0)
    
    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    last_course_added = models.DateTimeField('Последний добавленный курс', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['-courses_count']),  # Для сортировки по популярности
            models.Index(fields=['-active_courses_count']),
            models.Index(fields=['-average_course_rating']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def update_counts(self):
        """Обновляет все вычисляемые поля"""
        from django.db.models import Count, Avg, Q
        
        # Получаем все курсы в категории и её подкатегориях
        categories = self.get_descendants(include_self=True)
        courses = Course.objects.filter(category__in=categories)
        
        # Подсчитываем общее количество курсов
        self.courses_count = courses.count()
        
        # Подсчитываем активные курсы
        self.active_courses_count = courses.filter(status='published').count()
        
        # Подсчитываем уникальных студентов
        self.total_students = Enrollment.objects.filter(
            course__in=courses
        ).values('student').distinct().count()
        
        # Вычисляем средний рейтинг
        avg_rating = courses.aggregate(avg=Avg('average_rating'))['avg']
        self.average_course_rating = round(avg_rating, 2) if avg_rating else 0
        
        # Обновляем дату последнего добавленного курса
        latest_course = courses.order_by('-created_at').first()
        if latest_course:
            self.last_course_added = latest_course.created_at
        
        self.save()

    def get_descendants(self, include_self=True):
        """Возвращает все подкатегории"""
        descendants = []
        if include_self:
            descendants.append(self)
        
        for child in self.children.all():
            descendants.extend(child.get_descendants())
        
        return descendants

    def get_course_statistics(self):
        """Возвращает статистику по курсам в категории"""
        return {
            'total_courses': self.courses_count,
            'active_courses': self.active_courses_count,
            'total_students': self.total_students,
            'average_rating': self.average_course_rating,
            'last_course_added': self.last_course_added,
        }

    def get_popular_courses(self, limit=5):
        """Возвращает популярные курсы в категории"""
        return Course.objects.filter(
            category__in=self.get_descendants(include_self=True),
            status='published'
        ).order_by('-students_count')[:limit]

class Tag(BaseModel):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class CourseUserRole(models.Model):
    """Промежуточная модель для связи пользователей с курсами и их ролями"""
    
    ROLE_CHOICES = [
        ('teacher', 'Преподаватель'),
        ('producer', 'Продюсер'),
        ('assistant', 'Ассистент'),
    ]

    DEFAULT_PERMISSIONS = {
        'teacher': {
            'can_edit_content': True,
            'can_manage_students': True,
            'can_view_analytics': True,
        },
        'producer': {
            'can_edit_content': True,
            'can_manage_students': True,
            'can_view_analytics': True,
            'can_manage_teachers': True,
            'can_manage_pricing': True,
            'can_manage_marketing': True,
        },
        'assistant': {
            'can_edit_content': False,
            'can_manage_students': True,
            'can_view_analytics': False,
        }
    }

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='user_roles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_roles')
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES)
    permissions = models.JSONField('Права доступа', default=dict, blank=True)
    is_primary = models.BooleanField('Основная роль', default=False)
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_course_roles')

    class Meta:
        verbose_name = 'Роль пользователя в курсе'
        verbose_name_plural = 'Роли пользователей в курсах'
        unique_together = ['course', 'user', 'role']
        indexes = [
            models.Index(fields=['course', 'role']),
            models.Index(fields=['user', 'role']),
        ]

    def __str__(self):
        return f'{self.user} - {self.get_role_display()} в курсе {self.course}'

    def save(self, *args, **kwargs):
        # Устанавливаем права доступа по умолчанию при создании
        if not self.permissions:
            self.permissions = self.DEFAULT_PERMISSIONS.get(self.role, {})
        
        # Если это основная роль, убираем этот статус у других ролей пользователя в этом курсе
        if self.is_primary:
            CourseUserRole.objects.filter(
                course=self.course,
                user=self.user,
            ).exclude(id=self.id).update(is_primary=False)
        
        super().save(*args, **kwargs)

    def has_permission(self, permission):
        """Проверяет наличие конкретного разрешения у роли"""
        return self.permissions.get(permission, False)

class Course(BaseModel):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый')
    ]
    
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('ky', 'Кыргызский'),
        ('en', 'Английский')
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На проверке'),
        ('published', 'Опубликован'),
        ('archived', 'В архиве')
    ]
    
    CURRENCY_CHOICES = [
        ('KGS', 'Кыргызский сом'),
        ('USD', 'Доллар США'),
        ('RUB', 'Российский рубль')
    ]

    TYPE_CHOICES = [
        ('free', 'Бесплатный'),
        ('paid', 'Платный'),
        ('public', 'Публичный')
    ]

    # Основная информация
    title = models.CharField('Название', max_length=200, db_index=True)
    slug = models.SlugField('URL', unique=True, db_index=True)
    description = RichTextField('Описание')
    excerpt = models.TextField('Краткое описание', blank=True)
    
    # Категоризация
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name='Категория',
        related_name='courses'
    )
    tags = models.ManyToManyField(
        Tag, 
        verbose_name='Теги', 
        blank=True,
        related_name='courses'
    )
    
    # Участники курса
    users = models.ManyToManyField(
        User,
        through='CourseUserRole',
        through_fields=('course', 'user'),
        related_name='participated_courses'
    )
    
    # Медиа
    cover_image = models.ImageField(
        'Обложка', 
        upload_to='courses/covers/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif']), validate_image_size],
        help_text='Рекомендуемый размер: 700x430px. Максимальный размер: 2MB'
    )
    video_intro = models.URLField(
        'Вводное видео',
        max_length=200,
        validators=[validate_video_url],
        null=True,
        blank=True,
        help_text='Поддерживаются ссылки с YouTube и Vimeo'
    )
    
    # Ценообразование
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    currency = models.CharField(
        'Валюта',
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='KGS'
    )
    discount_price = models.DecimalField(
        'Цена со скидкой',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    
    # Характеристики
    difficulty = models.CharField(
        'Сложность',
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner'
    )
    language = models.CharField(
        'Язык',
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='ru'
    )
    duration = models.PositiveIntegerField(
        'Длительность (в минутах)',
        default=0
    )
    
    # Статус и метаданные
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    type = models.CharField(
        'Тип курса',
        max_length=20,
        choices=TYPE_CHOICES,
        default='paid'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    published_at = models.DateTimeField('Дата публикации', null=True, blank=True)
    archived_at = models.DateTimeField('Дата архивации', null=True, blank=True)
    
    # Вычисляемые поля
    students_count = models.PositiveIntegerField('Количество студентов', default=0)
    reviews_count = models.PositiveIntegerField('Количество отзывов', default=0)
    average_rating = models.DecimalField(
        'Средний рейтинг',
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    total_lessons = models.PositiveIntegerField('Всего уроков', default=0)
    completion_rate = models.DecimalField(
        'Процент завершения',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'type', 'language']),
            models.Index(fields=['-average_rating', '-students_count']),
            models.Index(fields=['price', 'category']),
            models.Index(fields=['published_at', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Инвалидируем кеш при сохранении
        cache_keys = [
            f'course_details_{self.id}',
            f'course_modules_{self.id}',
            f'course_teachers_{self.id}',
            f'course_analytics_{self.id}',
        ]
        cache.delete_many(cache_keys)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Получает URL курса"""
        return reverse('course_detail', kwargs={'slug': self.slug})

    def get_primary_teacher(self):
        """Возвращает основного преподавателя курса"""
        cache_key = f'course_primary_teacher_{self.id}'
        teacher = cache.get(cache_key)
        
        if teacher is None:
            teacher = self.user_roles.filter(
                role='teacher',
                is_primary=True
            ).select_related('user').first()
            
            if teacher:
                cache.set(cache_key, teacher, 3600)  # кешируем на 1 час
                
        return teacher

    def get_teachers(self):
        """Возвращает всех преподавателей курса"""
        cache_key = f'course_teachers_{self.id}'
        teachers = cache.get(cache_key)
        
        if teachers is None:
            teachers = User.objects.filter(
                course_roles__course=self,
                course_roles__role='teacher'
            ).distinct()
            
            cache.set(cache_key, list(teachers), 3600)  # кешируем на 1 час
            
        return teachers

    def get_primary_producer(self):
        """Возвращает основного продюсера курса"""
        producer_role = self.user_roles.filter(
            role='producer',
            is_primary=True
        ).select_related('user').first()
        return producer_role.user if producer_role else None

    def get_producers(self):
        """Возвращает всех продюсеров курса"""
        return User.objects.filter(
            course_roles__course=self,
            course_roles__role='producer'
        ).distinct()

    def add_producer(self, user, is_primary=False, added_by=None):
        """Добавляет продюсера к курсу"""
        if not user.role == 'producer':
            raise ValidationError('Пользователь должен иметь роль продюсера')
        
        role, created = CourseUserRole.objects.get_or_create(
            course=self,
            user=user,
            role='producer',
            defaults={
                'is_primary': is_primary,
                'added_by': added_by
            }
        )
        
        if not created and role.is_primary != is_primary:
            role.is_primary = is_primary
            role.save()
        
        return role

    def remove_producer(self, user):
        """Удаляет продюсера из курса"""
        return self.user_roles.filter(
            user=user,
            role='producer'
        ).delete()

    def get_total_lessons(self):
        """Возвращает общее количество уроков"""
        if self.total_lessons > 0:
            return self.total_lessons
            
        self.total_lessons = sum(
            module.lessons.count() 
            for module in self.modules.all()
        )
        self.save(update_fields=['total_lessons'])
        
        return self.total_lessons

    def update_rating_stats(self):
        """Обновляет статистику рейтинга"""
        from django.db.models import Avg, Count
        
        stats = self.reviews.aggregate(
            avg_rating=Avg('rating'),
            count=Count('id')
        )
        
        self.average_rating = stats['avg_rating'] or 0
        self.reviews_count = stats['count']
        self.save(update_fields=['average_rating', 'reviews_count'])

    def update_student_stats(self):
        """Обновляет статистику студентов"""
        total_students = self.enrollments.count()
        completed_students = self.enrollments.filter(status='completed').count()
        
        self.students_count = total_students
        if total_students > 0:
            self.completion_rate = (completed_students / total_students) * 100
        
        self.save(update_fields=['students_count', 'completion_rate'])

    def is_ready_for_publication(self):
        """Проверяет, готов ли курс к публикации"""
        return all([
            self.modules.exists(),  # есть хотя бы один модуль
            self.get_total_lessons() > 0,  # есть уроки
            self.cover_image,  # есть обложка
            self.description,  # есть описание
            self.get_primary_teacher()  # есть основной преподаватель
        ])

class Module(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(BaseModel):
    CONTENT_TYPES = [
        ('video', 'Видео'),
        ('text', 'Текст'),
        ('test', 'Тест'),
        ('presentation', 'Презентация')
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название', max_length=200)
    content_type = models.CharField('Тип контента', max_length=20, choices=CONTENT_TYPES)
    content = RichTextField('Содержание')
    video_url = models.URLField('URL видео', null=True, blank=True, validators=[validate_video_url])
    file = models.FileField(
        'Файл',
        upload_to='courses/lessons/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'ppt', 'pptx'])]
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    duration_minutes = models.PositiveIntegerField('Продолжительность (в минутах)', null=True, blank=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']

    def __str__(self):
        return f"{self.module.course.title} - {self.module.title} - {self.title}"

    def clean(self):
        if self.content_type == 'video' and not self.video_url:
            raise ValidationError('Для видео-урока необходимо указать URL видео')
        if self.content_type == 'presentation' and not self.file:
            raise ValidationError('Для презентации необходимо загрузить файл')

class Review(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField('Отзыв')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['course', 'user']  # Один пользователь - один отзыв

    def __str__(self):
        return f"Отзыв от {self.user} на курс {self.course}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        self.course.update_rating_stats()

class Announcement(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField('Заголовок', max_length=200)
    content = RichTextField('Содержание')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Enrollment(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершен'),
        ('dropped', 'Отчислен')
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField('Дата зачисления', default=timezone.now)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    completed_at = models.DateTimeField('Дата завершения', null=True, blank=True)
    progress = models.PositiveIntegerField('Прогресс (%)', default=0, 
                                         validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_accessed = models.DateTimeField('Последний доступ', null=True, blank=True)

    class Meta:
        verbose_name = 'Зачисление'
        verbose_name_plural = 'Зачисления'
        unique_together = ['student', 'course']  # Студент может быть зачислен на курс только один раз

    def __str__(self):
        return f"{self.student} - {self.course}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Если новая запись
            self.enrolled_at = timezone.now()
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

class Promocode(BaseModel):
    code = models.CharField('Код', max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(
        'Процент скидки',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    valid_from = models.DateTimeField('Действует с')
    valid_until = models.DateTimeField('Действует до')
    max_uses = models.PositiveIntegerField('Максимальное количество использований')
    used_count = models.PositiveIntegerField('Использовано раз', default=0)
    courses = models.ManyToManyField(Course, related_name='promocodes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code

    def clean(self):
        if self.valid_until and self.valid_from and self.valid_until <= self.valid_from:
            raise ValidationError('Дата окончания должна быть позже даты начала')
        if self.discount_percent > 100:
            raise ValidationError('Процент скидки не может быть больше 100')
        if self.max_uses < self.used_count:
            raise ValidationError('Количество использований не может быть меньше уже использованных')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Promotion(BaseModel):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    discount_percent = models.PositiveIntegerField('Процент скидки')
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    courses = models.ManyToManyField(Course, related_name='promotions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.title

class CourseAnalytics(BaseModel):
    """
    Модель для хранения агрегированной аналитики курса
    """
    course = models.OneToOneField('Course', on_delete=models.CASCADE, related_name='analytics')
    views_count = models.PositiveIntegerField('Количество просмотров', default=0)
    completion_count = models.PositiveIntegerField('Количество завершений', default=0)
    completion_rate = models.DecimalField('Процент завершения', max_digits=5, decimal_places=2, default=0)
    total_ratings = models.PositiveIntegerField('Всего оценок', default=0)
    rating_sum = models.PositiveIntegerField('Сумма оценок', default=0)
    average_rating = models.DecimalField('Средний рейтинг', max_digits=3, decimal_places=2, default=0)
    revenue = models.DecimalField('Доход', max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Аналитика курса'
        verbose_name_plural = 'Аналитика курсов'
        indexes = [
            models.Index(fields=['course', '-updated_at']),
            models.Index(fields=['-views_count']),
            models.Index(fields=['-average_rating']),
            models.Index(fields=['-revenue']),
        ]

    def __str__(self):
        return f'Аналитика курса {self.course.title}'

class AnalyticsLog(BaseModel):
    """
    Модель для хранения детальных логов аналитики
    """
    EVENT_TYPES = (
        ('view', 'Просмотр'),
        ('complete', 'Завершение'),
        ('rate', 'Оценка'),
        ('purchase', 'Покупка'),
    )

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='analytics_logs')
    event_type = models.CharField('Тип события', max_length=10, choices=EVENT_TYPES)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='analytics_logs')
    timestamp = models.DateTimeField('Время события', auto_now_add=True)
    data = models.JSONField('Данные события', default=dict)

    class Meta:
        verbose_name = 'Лог аналитики'
        verbose_name_plural = 'Логи аналитики'
        indexes = [
            models.Index(fields=['course', '-timestamp']),
            models.Index(fields=['event_type', '-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]

    def __str__(self):
        return f'{self.get_event_type_display()} - {self.course.title} - {self.timestamp}'

class TrafficSource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    source = models.CharField('Источник', max_length=100)  # organic, facebook, instagram и т.д.
    utm_campaign = models.CharField('UTM кампания', max_length=100, blank=True)
    utm_content = models.CharField('UTM контент', max_length=100, blank=True)
    views_count = models.PositiveIntegerField('Количество просмотров', default=0)
    conversion_count = models.PositiveIntegerField('Количество конверсий', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Источник трафика'
        verbose_name_plural = 'Источники трафика'

    def __str__(self):
        return f"{self.source} - {self.course.title}"

class EmailCampaign(BaseModel):
    title = models.CharField('Название', max_length=200)
    subject = models.CharField('Тема письма', max_length=200)
    content = models.TextField('Содержание')
    courses = models.ManyToManyField(Course, related_name='email_campaigns')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField('Отправлено', null=True, blank=True)
    recipients_count = models.PositiveIntegerField('Количество получателей', default=0)
    opens_count = models.PositiveIntegerField('Количество открытий', default=0)
    clicks_count = models.PositiveIntegerField('Количество кликов', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Email кампания'
        verbose_name_plural = 'Email кампании'

    def __str__(self):
        return self.title

class Specialization(BaseModel):
    name = models.CharField('Название', max_length=100, db_index=True)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', unique=True, db_index=True)
    
    # Вычисляемые поля
    teachers_count = models.PositiveIntegerField('Количество преподавателей', default=0)
    courses_count = models.PositiveIntegerField('Количество курсов', default=0)
    total_students = models.PositiveIntegerField('Всего студентов', default=0)
    average_teacher_rating = models.DecimalField('Средний рейтинг преподавателей', 
                                               max_digits=3, decimal_places=2, default=0)
    
    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_trending = models.BooleanField('Популярная специализация', default=False)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['-teachers_count']),
            models.Index(fields=['-courses_count']),
            models.Index(fields=['-average_teacher_rating']),
            models.Index(fields=['is_trending', '-teachers_count']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def update_counts(self):
        """Обновляет все вычисляемые поля"""
        from django.db.models import Count, Avg
        
        # Получаем всех преподавателей специализации
        teachers = User.objects.filter(
            course_roles__role='teacher',
            profile__specializations=self
        ).distinct()
        
        # Подсчитываем количество преподавателей
        self.teachers_count = teachers.count()
        
        # Получаем все курсы специализации
        courses = Course.objects.filter(
            user_roles__user__in=teachers,
            user_roles__role='teacher'
        ).distinct()
        
        # Подсчитываем количество курсов
        self.courses_count = courses.count()
        
        # Подсчитываем уникальных студентов
        self.total_students = Enrollment.objects.filter(
            course__in=courses
        ).values('student').distinct().count()
        
        # Вычисляем средний рейтинг преподавателей
        avg_rating = teachers.aggregate(
            avg=Avg('profile__rating')
        )['avg']
        self.average_teacher_rating = round(avg_rating, 2) if avg_rating else 0
        
        # Обновляем trending статус
        self.is_trending = (
            self.teachers_count >= 5 and 
            self.courses_count >= 10 and 
            self.average_teacher_rating >= 4.0
        )
        
        self.save()

    def get_statistics(self):
        """Возвращает статистику специализации"""
        return {
            'teachers_count': self.teachers_count,
            'courses_count': self.courses_count,
            'total_students': self.total_students,
            'average_rating': self.average_teacher_rating,
            'is_trending': self.is_trending,
        }

    def get_top_teachers(self, limit=5):
        """Возвращает топ преподавателей специализации"""
        return User.objects.filter(
            course_roles__role='teacher',
            profile__specializations=self
        ).order_by('-profile__rating')[:limit]

    def get_popular_courses(self, limit=5):
        """Возвращает популярные курсы специализации"""
        return Course.objects.filter(
            user_roles__user__profile__specializations=self,
            user_roles__role='teacher',
            status='published'
        ).order_by('-students_count')[:limit]
