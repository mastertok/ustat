from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import Course
from core.models import BaseModel

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['course', 'user']
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Отзыв от {self.user.email} на курс {self.course.title}"

class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_replies')
    content = models.TextField('Ответ')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Ответ на отзыв'
        verbose_name_plural = 'Ответы на отзывы'
        ordering = ['created_at']

    def __str__(self):
        return f"Ответ от {self.user.email} на отзыв {self.review.id}"
