from django.db import models
from django.contrib import admin

class BaseModel(models.Model):
    """Базовая модель с общими полями"""
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        abstract = True

class BaseAdminConfig:
    """Базовая конфигурация для админки"""
    @classmethod
    def get_admin_class(cls, model_class):
        """Создает класс админки с настройками по умолчанию"""
        class AutoModelAdmin(admin.ModelAdmin):
            # Получаем все поля модели для отображения
            list_display = [field.name for field in model_class._meta.fields 
                          if not isinstance(field, models.TextField)]
            
            # Добавляем поиск по текстовым полям
            search_fields = [field.name for field in model_class._meta.fields 
                           if isinstance(field, (models.CharField, models.TextField))]
            
            # Добавляем фильтры по булевым полям и полям со choices
            list_filter = [field.name for field in model_class._meta.fields 
                         if isinstance(field, models.BooleanField) 
                         or getattr(field, 'choices', None) is not None]
            
            # Если есть поле created_at, добавляем иерархию по дате
            if 'created_at' in [field.name for field in model_class._meta.fields]:
                date_hierarchy = 'created_at'
            
            # Если есть поля title/name и slug, автоматически заполняем slug
            if all(field in [f.name for f in model_class._meta.fields] for field in ['slug', 'title']):
                prepopulated_fields = {'slug': ('title',)}
            elif all(field in [f.name for f in model_class._meta.fields] for field in ['slug', 'name']):
                prepopulated_fields = {'slug': ('name',)}
        
        return AutoModelAdmin
