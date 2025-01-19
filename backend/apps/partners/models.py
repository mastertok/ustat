from django.db import models


class Partner(models.Model):
    name = models.CharField('Название', max_length=255)
    logo = models.ImageField('Логотип', upload_to='partners/logos/')
    website = models.URLField('Веб-сайт')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['name']

    def __str__(self):
        return self.name
