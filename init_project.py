import os
import sys
import django
from django.core.management import call_command

def init_project():
    """Инициализация проекта: удаление БД, миграции и загрузка демо-данных"""
    print("1. Удаление старой базы данных...")
    try:
        os.remove("db.sqlite3")
        print("База данных успешно удалена")
    except FileNotFoundError:
        print("База данных не существует")

    print("\n2. Применение миграций...")
    call_command('migrate')
    print("Миграции успешно применены")

    print("\n3. Загрузка демо-данных...")
    try:
        call_command('loaddata', 'demo/fixtures/initial_data.json')
        print("Демо-данные успешно загружены")
    except Exception as e:
        print(f"Ошибка при загрузке демо-данных: {e}")

    print("\nИнициализация проекта завершена!")
    print("\nТеперь вы можете:")
    print("1. Запустить сервер командой: python manage.py runserver")
    print("2. Создать суперпользователя командой: python manage.py createsuperuser")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ustat.settings')
    django.setup()
    init_project()
