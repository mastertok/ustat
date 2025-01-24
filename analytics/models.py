from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import User
from courses.models import Course, Lesson
from core.models import BaseModel

# Create your models here.

class CourseView(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_views')
    viewed_at = models.DateTimeField('Дата просмотра', auto_now_add=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Просмотр курса'
        verbose_name_plural = 'Просмотры курсов'
        indexes = [
            models.Index(fields=['course', 'user']),
            models.Index(fields=['viewed_at']),
        ]

    def __str__(self):
        return f"{self.user.email} просмотрел {self.course.title}"

class LessonProgress(models.Model):
    STATUSES = (
        ('not_started', 'Не начат'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('failed', 'Не пройден'),
    )

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    status = models.CharField('Статус', max_length=20, choices=STATUSES, default='not_started')
    progress = models.PositiveSmallIntegerField('Прогресс', default=0)
    attempts = models.PositiveSmallIntegerField('Количество попыток', default=0)
    started_at = models.DateTimeField('Начало', null=True, blank=True)
    completed_at = models.DateTimeField('Завершение', null=True, blank=True)
    last_activity = models.DateTimeField('Последняя активность', auto_now=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Прогресс урока'
        verbose_name_plural = 'Прогресс уроков'
        indexes = [
            models.Index(fields=['lesson', 'user']),
            models.Index(fields=['status', 'completed_at']),
        ]
        unique_together = ['lesson', 'user']

    def __str__(self):
        return f'{self.user.email} - {self.lesson} ({self.get_status_display()})'

class Revenue(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='revenues')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    date = models.DateField('Дата')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Доход'
        verbose_name_plural = 'Доходы'
        indexes = [
            models.Index(fields=['course', 'date']),
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        return f'Доход {self.amount} от {self.course.title} ({self.date})'
