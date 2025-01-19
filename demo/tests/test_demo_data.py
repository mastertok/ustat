import pytest
from django.core.management import call_command
from accounts.models import User, TeacherProfile
from courses.models import Course, Category
from reviews.models import Review

@pytest.mark.django_db
class TestDemoData:
    def test_demo_data_loaded(self):
        """Проверяет, что демо-данные успешно загружаются"""
        # Загружаем демо-данные
        call_command('loaddata', 'demo/fixtures/demo_data.json')
        
        # Проверяем количество созданных объектов
        assert User.objects.filter(role='teacher').count() == 3, "Должно быть 3 учителя"
        assert TeacherProfile.objects.count() == 3, "Должно быть 3 профиля учителей"
        assert Course.objects.count() == 3, "Должно быть 3 курса"
        assert Review.objects.count() == 1, "Должен быть 1 отзыв"
        assert Category.objects.count() == 3, "Должно быть 3 категории"
        
        # Проверяем конкретные объекты
        # Проверяем учителей
        assert User.objects.filter(username='teacher1').exists(), "Должен существовать teacher1"
        assert User.objects.filter(username='teacher2').exists(), "Должен существовать teacher2"
        assert User.objects.filter(username='teacher3').exists(), "Должен существовать teacher3"
        
        # Проверяем профили учителей
        assert TeacherProfile.objects.filter(slug='aigul-asanova').exists(), "Должен существовать профиль Айгуль"
        assert TeacherProfile.objects.filter(slug='bakyt-eshmatov').exists(), "Должен существовать профиль Бакыта"
        assert TeacherProfile.objects.filter(slug='chynara-jumabaeva').exists(), "Должен существовать профиль Чынары"
        
        # Проверяем категории
        assert Category.objects.filter(slug='mathematics').exists(), "Должна существовать категория математики"
        assert Category.objects.filter(slug='english').exists(), "Должна существовать категория английского"
        assert Category.objects.filter(slug='programming').exists(), "Должна существовать категория программирования"
        
        # Проверяем курсы
        assert Course.objects.filter(slug='ort-math-prep').exists(), "Должен существовать курс ОРТ"
        assert Course.objects.filter(slug='ielts-academic-prep').exists(), "Должен существовать курс IELTS"
        assert Course.objects.filter(slug='python-for-beginners').exists(), "Должен существовать курс Python"
        
        # Проверяем отзыв
        review = Review.objects.first()
        assert review is not None, "Должен существовать хотя бы один отзыв"
        assert review.rating == 5, "Рейтинг отзыва должен быть 5"
        assert review.course.slug == 'ort-math-prep', "Отзыв должен быть к курсу ОРТ"
        
        # Проверяем связи между объектами
        for course in Course.objects.all():
            assert course.teacher is not None, "У каждого курса должен быть учитель"
            assert course.category is not None, "У каждого курса должна быть категория"
            assert course.price > 0, "У каждого курса должна быть цена больше 0"
            assert course.currency == 'KGS', "Валюта курса должна быть KGS"
            assert course.status == 'published', "Статус курса должен быть published"
            assert course.course_type == 'paid', "Тип курса должен быть paid"
