import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ustat.settings')

# Создаем экземпляр приложения Celery
app = Celery('ustat')

# Загружаем настройки из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим и регистрируем задачи из установленных приложений Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """
    Тестовая задача для проверки работы Celery
    """
    print(f'Request: {self.request!r}')
