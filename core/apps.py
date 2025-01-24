from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Ядро'

    def ready(self):
        """
        Импортируем сигналы при запуске приложения
        """
        import core.signals  # noqa
