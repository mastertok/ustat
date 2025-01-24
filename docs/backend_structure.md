 # Структура бэкенда Устат

## 1. ORM Структура

### 1.1. Accounts (Система пользователей)

#### User Model
```python
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('producer', 'Продюсер'),
        ('admin', 'Администратор')
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, validators=[phone_regex])
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_verified'])
        ]
```

#### Profile Model
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(blank=True)
    custom_url = models.SlugField(unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    courses_count = models.PositiveIntegerField(default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'На проверке'),
            ('verified', 'Подтвержден'),
            ('rejected', 'Отклонен')
        ]
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['custom_url']),
            models.Index(fields=['-rating']),
            models.Index(fields=['verification_status'])
        ]
```

#### Education Model
```python
class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-end_date']
        indexes = [
            models.Index(fields=['profile', '-end_date'])
        ]
```

#### WorkExperience Model
```python
class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-end_date']
        indexes = [
            models.Index(fields=['profile', '-end_date'])
        ]
```

### 1.2. Courses (Система курсов)

#### Category Model
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent'])
        ]
```

#### Course Model
```python
class Course(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На проверке'),
        ('published', 'Опубликован'),
        ('archived', 'В архиве')
    ]
    
    TYPE_CHOICES = [
        ('video', 'Видео курс'),
        ('text', 'Текстовый курс'),
        ('mixed', 'Смешанный')
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый')
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=settings.CURRENCIES)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag')
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    preview_video = models.URLField(blank=True)
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00
    )
    students_count = models.PositiveIntegerField(default=0)
    total_lessons = models.PositiveIntegerField(default=0)
    duration_hours = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['-average_rating'])
        ]
```

#### Module Model
```python
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['course', 'order'])
        ]
        unique_together = ['course', 'order']
```

#### Lesson Model
```python
class Lesson(models.Model):
    CONTENT_TYPES = [
        ('video', 'Видео'),
        ('text', 'Текст'),
        ('quiz', 'Тест'),
        ('assignment', 'Задание')
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    file = models.FileField(upload_to='lesson_files/', blank=True)
    order = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['module', 'order']),
            models.Index(fields=['content_type'])
        ]
        unique_together = ['module', 'order']
```

#### CourseUserRole Model
```python
class CourseUserRole(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Преподаватель'),
        ('producer', 'Продюсер'),
        ('assistant', 'Ассистент')
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    permissions = models.JSONField(default=dict)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['course', 'user', 'role']
        indexes = [
            models.Index(fields=['course', 'role']),
            models.Index(fields=['user', 'role'])
        ]
```

### 1.3. Analytics (Система аналитики)

#### LessonProgress Model
```python
class LessonProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начат'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен')
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    progress = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['lesson', 'user']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['lesson', 'status']),
            models.Index(fields=['-last_activity'])
        ]
```

#### CourseView Model
```python
class CourseView(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['course', '-viewed_at']),
            models.Index(fields=['user', '-viewed_at'])
        ]
```

#### Revenue Model
```python
class Revenue(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=settings.CURRENCIES)
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('sale', 'Продажа'),
            ('refund', 'Возврат'),
            ('affiliate', 'Партнерская программа')
        ]
    )
    date = models.DateField()
    details = models.JSONField(default=dict)
    
    class Meta:
        indexes = [
            models.Index(fields=['course', '-date']),
            models.Index(fields=['-date']),
            models.Index(fields=['transaction_type'])
        ]
```

### 1.4. Reviews (Система отзывов)

#### Review Model
```python
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['course', 'user']
        indexes = [
            models.Index(fields=['course', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_verified'])
        ]
```

### 1.5. Payments (Система платежей)

#### Payment Model
```python
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('completed', 'Оплачен'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возврат')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=settings.CURRENCIES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['course', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_id'])
        ]
```

## 2. Основные модули

### 1.1. Accounts (Система пользователей)

#### Модели:
1. **User**
   - Кастомная модель пользователя
   - Роли: student, teacher, producer, admin
   - Поля:
     - email (EmailField, unique)
     - first_name (CharField)
     - last_name (CharField)
     - role (CharField, choices)
     - phone (CharField)
     - is_verified (BooleanField)

2. **Profile**
   - Расширенный профиль пользователя
   - Поля:
     - user (OneToOneField → User)
     - avatar (ImageField)
     - bio (TextField)
     - custom_url (SlugField, unique)
     - rating (DecimalField)
     - courses_count (IntegerField)
     - reviews_count (IntegerField)
     - verification_status (CharField)

3. **Education**
   - Образование пользователя
   - Поля:
     - profile (ForeignKey → Profile)
     - institution (CharField)
     - degree (CharField)
     - field_of_study (CharField)
     - start_date (DateField)
     - end_date (DateField)

4. **WorkExperience**
   - Опыт работы
   - Поля:
     - profile (ForeignKey → Profile)
     - company (CharField)
     - position (CharField)
     - description (TextField)
     - start_date (DateField)
     - end_date (DateField)

### 1.2. Courses (Система курсов)

#### Модели:
1. **Course**
   - Основная модель курса
   - Поля:
     - title (CharField)
     - slug (SlugField)
     - description (TextField)
     - status (CharField, choices)
     - type (CharField, choices)
     - difficulty (CharField, choices)
     - language (CharField, choices)
     - price (DecimalField)
     - currency (CharField, choices)
     - category (ForeignKey → Category)
     - tags (ManyToManyField → Tag)
     - average_rating (DecimalField)
     - students_count (IntegerField)
     - total_lessons (IntegerField)
     - duration_hours (IntegerField)

2. **Module**
   - Структурная единица курса
   - Поля:
     - course (ForeignKey → Course)
     - title (CharField)
     - description (TextField)
     - order (IntegerField)

3. **Lesson**
   - Урок в модуле
   - Поля:
     - module (ForeignKey → Module)
     - title (CharField)
     - content_type (CharField, choices)
     - content (RichTextField)
     - video_url (URLField)
     - file (FileField)
     - order (IntegerField)
     - duration_minutes (IntegerField)

4. **CourseUserRole**
   - Роли пользователей в курсе
   - Поля:
     - course (ForeignKey → Course)
     - user (ForeignKey → User)
     - role (CharField, choices)
     - permissions (JSONField)
     - is_primary (BooleanField)

### 1.3. Analytics (Система аналитики)

#### Модели:
1. **LessonProgress**
   - Отслеживание прогресса
   - Поля:
     - lesson (ForeignKey → Lesson)
     - user (ForeignKey → User)
     - status (CharField, choices)
     - progress (IntegerField)
     - attempts (IntegerField)
     - started_at (DateTimeField)
     - completed_at (DateTimeField)

2. **CourseView**
   - Статистика просмотров
   - Поля:
     - course (ForeignKey → Course)
     - user (ForeignKey → User)
     - viewed_at (DateTimeField)

3. **Revenue**
   - Финансовая аналитика
   - Поля:
     - course (ForeignKey → Course)
     - amount (DecimalField)
     - date (DateField)

## 2. API Endpoints

### 2.1. Accounts API
```
/api/auth/
├── login/ [POST]
├── register/ [POST]
├── verify-email/ [POST]
└── reset-password/ [POST]

/api/profiles/
├── me/ [GET, PUT]
├── <id>/ [GET]
└── custom-url/ [GET, PUT]

/api/teachers/
├── check-url/ [GET]
└── <custom_url>/
    ├── profile/ [GET]
    └── courses/ [GET]
```

### 2.2. Courses API
```
/api/courses/
├── [GET, POST]
├── <id>/
│   ├── [GET, PUT, DELETE]
│   ├── enroll/ [POST]
│   ├── modules/ [GET, POST]
│   └── analytics/ [GET]
└── search/ [GET]

/api/modules/
├── <id>/
│   ├── [GET, PUT, DELETE]
│   └── lessons/ [GET, POST]
└── reorder/ [POST]

/api/lessons/
└── <id>/
    ├── [GET, PUT, DELETE]
    └── progress/ [GET, POST]
```

### 2.3. Analytics API
```
/api/analytics/
├── revenue/ [GET]
├── progress/ [GET]
└── views/ [GET]
```

## 3. Роли и права доступа

### 3.1. Студент (student)
✅ Разрешено:
- Просмотр каталога курсов
- Запись на курсы
- Просмотр уроков
- Отслеживание прогресса
- Написание отзывов

❌ Запрещено:
- Создание курсов
- Доступ к админ-панели
- Просмотр финансовой статистики

### 3.2. Преподаватель (teacher)
✅ Разрешено:
- Создание и редактирование своих курсов
- Просмотр статистики по своим курсам
- Управление своим профилем
- Настройка custom_url

❌ Запрещено:
- Редактирование чужих курсов
- Доступ к глобальной статистике
- Управление другими пользователями

### 3.3. Продюсер (producer)
✅ Разрешено:
- Управление множеством курсов
- Назначение преподавателей
- Просмотр финансовой статистики
- Управление маркетингом
- Установка цен и акций

❌ Запрещено:
- Доступ к системным настройкам
- Управление администраторами

### 3.4. Администратор (admin)
✅ Разрешено:
- Полный доступ ко всем функциям
- Управление пользователями
- Системные настройки
- Доступ к логам и мониторингу

## 4. Безопасность

### 4.1. Аутентификация
- JWT токены для API
- Сессии для веб-интерфейса
- Верификация email
- Сброс пароля через email

### 4.2. Авторизация
- Ролевая модель доступа
- Проверка прав на уровне представлений
- Проверка владельца ресурса

### 4.3. Защита данных
- Хэширование паролей
- HTTPS для всех запросов
- Защита от CSRF
- Rate limiting для API

## 5. Кэширование

### 5.1. Redis Cache
- Кэширование частых запросов
- Хранение сессий
- Rate limiting

### 5.2. Кэшируемые данные
- Каталог курсов
- Профили преподавателей
- Статистика курсов
- Меню категорий

## 6. Очереди задач (Celery)

### 6.1. Асинхронные задачи
- Отправка email
- Генерация отчетов
- Обработка видео
- Обновление статистики

### 6.2. Периодические задачи
- Очистка устаревших данных
- Обновление рейтингов
- Создание бэкапов
- Проверка активности пользователей

## 7. Мониторинг

### 7.1. Prometheus + Grafana
- Метрики производительности
- Мониторинг ошибок
- Статистика запросов
- Использование ресурсов

### 7.2. Логирование
- Структурированные логи
- Ротация логов
- Алерты при критических ошибках

## 8. Тестирование

### 8.1. Unit Tests
- Тесты моделей
- Тесты представлений
- Тесты сериализаторов
- Тесты форм

### 8.2. Integration Tests
- API тесты
- Тесты бизнес-логики
- Тесты авторизации
- Тесты кэширования

### 8.3. Performance Tests
- Нагрузочное тестирование
- Тесты производительности
- Тесты масштабируемости

## 9. Развертывание

### 9.1. Production окружение
- Gunicorn + Nginx
- PostgreSQL
- Redis
- Celery

### 9.2. CI/CD
- Автоматические тесты
- Линтинг кода
- Проверка безопасности
- Автоматический деплой

## 10. Документация

### 10.1. API Documentation
- OpenAPI (Swagger)
- Postman коллекции
- Примеры запросов

### 10.2. Code Documentation
- Docstrings
- Type hints
- README файлы
- Комментарии к сложной логике

## 11. Расширенное API и масштабирование

### 11.1. Фильтрация курсов

#### API Endpoints
```python
# courses/api/views.py
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    
    filterset_fields = {
        'price': ['gte', 'lte', 'exact'],
        'language': ['exact', 'in'],
        'average_rating': ['gte', 'lte'],
        'duration_hours': ['gte', 'lte'],
        'difficulty': ['exact'],
        'category': ['exact'],
        'type': ['exact'],
        'status': ['exact']
    }
    
    ordering_fields = [
        'price',
        'created_at',
        'average_rating',
        'students_count',
        'duration_hours'
    ]
    
    search_fields = [
        'title',
        'description',
        'teacher__first_name',
        'teacher__last_name'
    ]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получение рекомендованных курсов"""
        featured = self.get_queryset().filter(
            status='published',
            average_rating__gte=4.0
        ).order_by('-students_count')[:10]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def price_ranges(self, request):
        """Получение диапазонов цен для фильтрации"""
        ranges = {
            'min_price': Course.objects.filter(
                status='published'
            ).aggregate(Min('price'))['price__min'],
            'max_price': Course.objects.filter(
                status='published'
            ).aggregate(Max('price'))['price__max'],
            'ranges': [
                {'min': 0, 'max': 1000, 'label': 'До 1000'},
                {'min': 1000, 'max': 5000, 'label': '1000 - 5000'},
                {'min': 5000, 'max': 10000, 'label': '5000 - 10000'},
                {'min': 10000, 'max': None, 'label': 'От 10000'}
            ]
        }
        return Response(ranges)
```

#### Примеры запросов
```
# Фильтрация по цене и рейтингу
GET /api/courses/?price_min=1000&price_max=5000&average_rating_min=4.0

# Фильтрация по языку и длительности
GET /api/courses/?language=ru&duration_hours_min=10

# Сортировка по рейтингу и цене
GET /api/courses/?ordering=-average_rating,price

# Поиск по названию и описанию
GET /api/courses/?search=python
```

### 11.2. Горизонтальное масштабирование

#### Конфигурация баз данных
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ustat_main',
        'USER': 'ustat_user',
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    },
    'analytics': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ustat_analytics',
        'USER': 'analytics_user',
        'PASSWORD': env('ANALYTICS_DB_PASSWORD'),
        'HOST': env('ANALYTICS_DB_HOST'),
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = ['core.routers.AnalyticsRouter']
```

#### Маршрутизация баз данных
```python
# core/routers.py
class AnalyticsRouter:
    """
    Маршрутизатор для разделения аналитических данных
    """
    analytics_models = {
        'CourseView',
        'Revenue',
        'LessonProgress',
        'UserActivity'
    }

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.analytics_models:
            return 'analytics'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.analytics_models:
            return 'analytics'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.analytics_models:
            return db == 'analytics'
        return db == 'default'
```

### 11.3. CDN интеграция

#### Конфигурация CDN
```python
# settings.py
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Статические файлы
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'core.storage.StaticStorage'

# Медиа файлы
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'core.storage.MediaStorage'

# Настройки для видео
VIDEO_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/video/'
VIDEO_FILE_STORAGE = 'core.storage.VideoStorage'
```

#### Кастомные классы хранилища
```python
# core/storage.py
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True
    
class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'private'
    file_overwrite = False
    
class VideoStorage(S3Boto3Storage):
    location = 'video'
    default_acl = 'private'
    file_overwrite = False
    
    def url(self, name, parameters=None, expire=300):
        """
        Генерация временных URL для видео
        """
        return super().url(name, parameters={'ResponseContentType': 'video/mp4'}, expire=expire)
```

#### Middleware для CDN
```python
# core/middleware.py
class CDNProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if 'Content-Type' in response and response['Content-Type'].startswith('video/'):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Range'
            response['Accept-Ranges'] = 'bytes'
        
        return response
```

#### Использование в моделях
```python
# courses/models.py
class Course(models.Model):
    # ... остальные поля ...
    
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/',
        storage=MediaStorage()
    )
    preview_video = models.FileField(
        upload_to='course_previews/',
        storage=VideoStorage(),
        blank=True
    )
    
    def get_video_url(self):
        """
        Получение временного URL для видео
        """
        if self.preview_video:
            return VideoStorage().url(
                self.preview_video.name,
                expire=3600  # URL действителен 1 час
            )
        return None
```

### 11.4. Кэширование и оптимизация

#### Настройка Redis для кэширования
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        }
    }
}

# Кэширование запросов к API
REST_FRAMEWORK = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15,  # 15 минут
    'DEFAULT_CACHE_METHODS': ['GET', 'HEAD'],
    'DEFAULT_CACHE_KEY_FUNCTION': 'core.cache.custom_cache_key'
}
```

#### Оптимизация запросов
```python
# courses/views.py
class CourseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Course.objects.select_related(
            'category',
            'teacher'
        ).prefetch_related(
            'tags',
            Prefetch(
                'modules',
                queryset=Module.objects.prefetch_related(
                    Prefetch(
                        'lessons',
                        queryset=Lesson.objects.order_by('order')
                    )
                ).order_by('order')
            )
        )
        
        if self.action == 'list':
            # Для списка курсов загружаем меньше данных
            queryset = queryset.defer(
                'description',
                'requirements',
                'target_audience'
            )
            
        return queryset.filter(status='published')
```