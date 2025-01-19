from django.db import models
from accounts.models import User
from courses.models import Course, Lesson

# Create your models here.

class CourseView(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_views')
    viewed_at = models.DateTimeField('Дата просмотра', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Просмотр курса'
        verbose_name_plural = 'Просмотры курсов'

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    watched_duration = models.PositiveIntegerField('Просмотрено минут', default=0)
    is_completed = models.BooleanField('Завершен', default=False)
    last_watched = models.DateTimeField('Последний просмотр', auto_now=True)
    
    class Meta:
        verbose_name = 'Прогресс урока'
        verbose_name_plural = 'Прогресс уроков'
        unique_together = ['user', 'lesson']

class Revenue(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='revenues')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    date = models.DateField('Дата')
    
    class Meta:
        verbose_name = 'Доход'
        verbose_name_plural = 'Доходы'
        
    def __str__(self):
        return f"Доход от {self.course.title} за {self.date}"
