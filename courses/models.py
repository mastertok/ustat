from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from accounts.models import TeacherProfile, ProducerProfile, User
from core.models import AutoRegisterAdmin

def validate_video_url(value):
    """Валидация URL видео (YouTube, Vimeo)"""
    if not any(platform in value.lower() for platform in ['youtube.com', 'youtu.be', 'vimeo.com']):
        raise ValidationError('URL должен быть с YouTube или Vimeo')

def validate_image_size(value):
    """Валидация размера изображения (макс. 2MB)"""
    if value.size > 2 * 1024 * 1024:
        raise ValidationError('Максимальный размер изображения 2MB')

class Category(AutoRegisterAdmin, models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='Родительская категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Tag(AutoRegisterAdmin, models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class Course(AutoRegisterAdmin, models.Model):
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
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = RichTextField('Описание')
    excerpt = models.TextField('Краткое описание', blank=True)
    
    # Категоризация
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    
    # Преподаватели
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, 
                               verbose_name='Преподаватель')
    producer = models.ForeignKey(ProducerProfile, on_delete=models.SET_NULL, null=True, blank=True, 
                                verbose_name='Продюсер')
    
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
    
    # Настройки курса
    max_students = models.PositiveIntegerField(
        'Максимальное количество студентов',
        default=0,
        help_text='0 - без ограничений'
    )
    difficulty_level = models.CharField(
        'Уровень сложности',
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner'
    )
    language = models.CharField(
        'Язык курса',
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='ru'
    )
    duration_minutes = models.PositiveIntegerField(
        'Продолжительность (в минутах)',
        null=True,
        blank=True
    )
    
    # Функциональность
    enable_qa = models.BooleanField('Включить вопросы и ответы', default=True)
    enable_announcements = models.BooleanField('Включить анонсы', default=True)
    enable_reviews = models.BooleanField('Включить отзывы', default=True)
    
    # Цена и тип
    course_type = models.CharField('Тип курса', max_length=10, choices=TYPE_CHOICES, default='paid')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0)
    currency = models.CharField('Валюта', max_length=3, choices=CURRENCY_CHOICES, default='KGS')
    discount_price = models.DecimalField(
        'Цена со скидкой',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Статистика
    sales_count = models.PositiveIntegerField('Количество продаж', default=0)
    average_rating = models.DecimalField('Средний рейтинг', max_digits=3, decimal_places=2, default=0)
    reviews_count = models.PositiveIntegerField('Количество отзывов', default=0)
    
    # Статус
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # SEO
    seo_title = models.CharField('SEO заголовок', max_length=200, blank=True)
    seo_description = models.TextField('SEO описание', blank=True)
    seo_keywords = models.CharField('SEO ключевые слова', max_length=500, blank=True)
    
    # Даты
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now)
    published_at = models.DateTimeField('Дата публикации', null=True, blank=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Если объект создается впервые
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    
    def update_rating(self):
        """Обновляет средний рейтинг курса"""
        avg_rating = self.course_reviews.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = round(avg_rating, 2) if avg_rating else 0
        self.reviews_count = self.course_reviews.count()
        self.save()
    
    def increment_sales(self):
        """Увеличивает счетчик продаж"""
        self.sales_count += 1
        self.save()
    
    def get_absolute_url(self):
        """Возвращает URL курса"""
        from django.urls import reverse
        return reverse('course_detail', kwargs={'slug': self.slug})

class Module(AutoRegisterAdmin, models.Model):
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

class Lesson(AutoRegisterAdmin, models.Model):
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

class Review(AutoRegisterAdmin, models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
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
        self.course.update_rating()

class Announcement(AutoRegisterAdmin, models.Model):
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

class Enrollment(AutoRegisterAdmin, models.Model):
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

class Promocode(AutoRegisterAdmin, models.Model):
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
    created_by = models.ForeignKey(ProducerProfile, on_delete=models.CASCADE)
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

class Promotion(AutoRegisterAdmin, models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    discount_percent = models.PositiveIntegerField('Процент скидки')
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    courses = models.ManyToManyField(Course, related_name='promotions')
    created_by = models.ForeignKey(ProducerProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.title

class CourseAnalytics(AutoRegisterAdmin, models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    views_count = models.PositiveIntegerField('Количество просмотров', default=0)
    cart_adds_count = models.PositiveIntegerField('Добавлено в корзину', default=0)
    purchases_count = models.PositiveIntegerField('Количество покупок', default=0)

    class Meta:
        verbose_name = 'Аналитика курса'
        verbose_name_plural = 'Аналитика курсов'

    def __str__(self):
        return f"Аналитика: {self.course.title}"

class TrafficSource(AutoRegisterAdmin, models.Model):
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

class EmailCampaign(AutoRegisterAdmin, models.Model):
    title = models.CharField('Название', max_length=200)
    subject = models.CharField('Тема письма', max_length=200)
    content = models.TextField('Содержание')
    courses = models.ManyToManyField(Course, related_name='email_campaigns')
    created_by = models.ForeignKey(ProducerProfile, on_delete=models.CASCADE)
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
