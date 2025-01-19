from django.db import models
from django.contrib import admin

class AutoRegisterAdmin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """Автоматически регистрирует модель в админке при её создании"""
        super().__init_subclass__(**kwargs)
        
        # Пропускаем абстрактные модели
        if not cls._meta.abstract:
            # Создаем класс админки с настройками по умолчанию
            class AutoModelAdmin(admin.ModelAdmin):
                # Получаем все поля модели для отображения
                list_display = [field.name for field in cls._meta.fields 
                              if not isinstance(field, models.TextField)]
                
                # Добавляем поиск по текстовым полям
                search_fields = [field.name for field in cls._meta.fields 
                               if isinstance(field, (models.CharField, models.TextField))]
                
                # Добавляем фильтры по булевым полям и полям со choices
                list_filter = [field.name for field in cls._meta.fields 
                             if isinstance(field, (models.BooleanField)) 
                             or field.choices is not None]
                
                # Если есть поле created_at, добавляем иерархию по дате
                if 'created_at' in [field.name for field in cls._meta.fields]:
                    date_hierarchy = 'created_at'
                
                # Если есть поля title/name и slug, автоматически заполняем slug
                if 'slug' in [field.name for field in cls._meta.fields]:
                    if 'title' in [field.name for field in cls._meta.fields]:
                        prepopulated_fields = {'slug': ('title',)}
                    elif 'name' in [field.name for field in cls._meta.fields]:
                        prepopulated_fields = {'slug': ('name',)}

            # Регистрируем модель в админке
            try:
                admin.site.register(cls, AutoModelAdmin)
            except admin.sites.AlreadyRegistered:
                pass  # Пропускаем, если модель уже зарегистрирована
