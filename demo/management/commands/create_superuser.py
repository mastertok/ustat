from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает суперпользователя с предустановленными данными'

    def handle(self, *args, **options):
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create(
                    username='admin',
                    email='admin@ustat.kg',
                    password=make_password('admin12345'),
                    is_staff=True,
                    is_superuser=True,
                    role='admin'
                )
                self.stdout.write(self.style.SUCCESS('Суперпользователь успешно создан!'))
                self.stdout.write('Логин: admin')
                self.stdout.write('Пароль: admin12345')
            else:
                self.stdout.write(self.style.WARNING('Суперпользователь уже существует'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при создании суперпользователя: {str(e)}'))
