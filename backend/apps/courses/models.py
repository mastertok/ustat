from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    icon = models.CharField('Иконка', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('kg', 'Кыргызский'),
        ('en', 'Английский'),
    ]

    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True, default='')
    description = models.TextField('Описание')
    meta_title = models.CharField('Meta заголовок', max_length=255, blank=True, default='')
    meta_description = models.TextField('Meta описание', blank=True, default='')
    meta_keywords = models.CharField('Meta ключевые слова', max_length=255, blank=True, default='')
    image = models.ImageField('Изображение', upload_to='courses/images/')
    preview_video = models.URLField('Превью видео', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    duration = models.CharField('Продолжительность', max_length=50)
    level = models.CharField('Уровень', max_length=20, choices=LEVEL_CHOICES)
    language = models.CharField('Язык', max_length=2, choices=LANGUAGE_CHOICES, default='ru')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_courses', blank=True)
    students_count = models.IntegerField('Количество студентов', default=0)
    average_rating = models.DecimalField('Средний рейтинг', max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def update_rating(self):
        ratings = self.reviews.all().values_list('rating', flat=True)
        if ratings:
            self.average_rating = sum(ratings) / len(ratings)
            self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            # Словарь для транслитерации
            translit_dict = {
                'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
                'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            }
            
            # Транслитерация текста
            title_trans = ''.join(translit_dict.get(c.lower(), c.lower()) for c in self.title)
            # Создание slug
            self.slug = slugify(title_trans)

        if not self.meta_title:
            self.meta_title = self.title

        if not self.meta_description:
            # Ограничиваем описание 160 символами для мета-тегов
            self.meta_description = self.description[:160]

        if not self.meta_keywords:
            # Генерируем ключевые слова из названия курса, категории и уровня
            keywords = [
                self.title,
                self.category.name if self.category else '',
                self.level,
                'онлайн курс',
                'обучение',
            ]
            self.meta_keywords = ', '.join(filter(None, keywords))

        super().save(*args, **kwargs)


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    video_url = models.URLField('Видео URL', blank=True)
    content = models.TextField('Контент')
    is_free = models.BooleanField('Бесплатный урок', default=False)
    duration = models.CharField('Продолжительность', max_length=50)
    order = models.PositiveIntegerField('Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']

    def __str__(self):
        return f"{self.module.course.title} - {self.module.title} - {self.title}"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['course', 'user']

    def __str__(self):
        return f"{self.course.title} - {self.user.username} - {self.rating}★"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.course.update_rating()
