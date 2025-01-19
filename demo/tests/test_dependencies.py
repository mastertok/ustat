import pytest
from django.contrib.auth import get_user_model
from accounts.models import TeacherProfile, ProducerProfile, Education, WorkExperience, Achievement, Specialization
from courses.models import Course, Category, Enrollment
from reviews.models import Review, Reply
import uuid

User = get_user_model()

def get_unique_slug():
    return f"slug_{uuid.uuid4().hex[:8]}"

@pytest.mark.django_db
class TestModelDependencies:
    def test_user_teacher_profile_dependency(self, teacher_user):
        """
        Тест зависимости между User и TeacherProfile:
        - При удалении User должен удаляться и профиль учителя
        """
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        user_id = teacher_user.id
        teacher_user.delete()
        
        assert not User.objects.filter(id=user_id).exists()
        assert not TeacherProfile.objects.filter(user_id=user_id).exists()
    
    def test_teacher_education_dependency(self, teacher_user):
        """
        Тест зависимости между TeacherProfile и Education:
        - При удалении профиля учителя должны удаляться все записи об образовании
        """
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        
        education = Education.objects.create(
            teacher=profile,
            institution='КНУ',
            degree='Бакалавр',
            field_of_study='Математика',
            start_date='2015-09-01',
            end_date='2019-06-30'
        )
        
        profile_id = profile.id
        profile.delete()
        
        assert not Education.objects.filter(teacher_id=profile_id).exists()
    
    def test_teacher_work_experience_dependency(self, teacher_user):
        """
        Тест зависимости между TeacherProfile и WorkExperience:
        - При удалении профиля учителя должны удаляться все записи об опыте работы
        """
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        
        work = WorkExperience.objects.create(
            teacher=profile,
            company='Школа №1',
            position='Учитель математики',
            start_date='2019-09-01',
            is_current=True
        )
        
        profile_id = profile.id
        profile.delete()
        
        assert not WorkExperience.objects.filter(teacher_id=profile_id).exists()
    
    def test_teacher_achievement_dependency(self, teacher_user):
        """
        Тест зависимости между TeacherProfile и Achievement:
        - При удалении профиля учителя должны удаляться все достижения
        """
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        
        achievement = Achievement.objects.create(
            teacher=profile,
            title='Лучший учитель года',
            date_received='2023-05-15',
            issuer='Министерство образования'
        )
        
        profile_id = profile.id
        profile.delete()
        
        assert not Achievement.objects.filter(teacher_id=profile_id).exists()
    
    def test_course_dependencies(self, teacher_user):
        """
        Тест зависимостей для курсов:
        - При удалении учителя должны удаляться его курсы
        - При удалении курса должны удаляться все записи на курс
        - При удалении курса должны удаляться все отзывы
        """
        # Создаем профиль учителя
        teacher_profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        
        # Создаем продюсера
        producer_user = User.objects.create_user(
            username=f"producer_{uuid.uuid4().hex[:8]}",
            password='password123',
            role='producer'
        )
        producer_profile = ProducerProfile.objects.create(user=producer_user)
        
        # Создаем категорию
        category = Category.objects.create(
            name='Математика',
            slug=get_unique_slug()
        )
        
        # Создаем курс
        course = Course.objects.create(
            title='Алгебра',
            slug=get_unique_slug(),
            teacher=teacher_profile,
            producer=producer_profile,
            category=category,
            price=1000,
            status='published'
        )
        
        # Создаем студента
        student = User.objects.create_user(
            username=f"student_{uuid.uuid4().hex[:8]}",
            password='password123',
            role='student'
        )
        
        # Создаем запись на курс
        enrollment = Enrollment.objects.create(
            student=student,
            course=course
        )
        
        # Создаем отзыв
        review = Review.objects.create(
            course=course,
            user=student,
            rating=5,
            comment='Отличный курс!'
        )
        
        # Создаем ответ на отзыв
        reply = Reply.objects.create(
            review=review,
            user=teacher_user,
            content='Спасибо за отзыв!'
        )
        
        # Проверяем каскадное удаление
        course_id = course.id
        review_id = review.id
        course.delete()
        
        # Проверяем, что все связанные объекты удалены
        assert not Enrollment.objects.filter(course_id=course_id).exists()
        assert not Review.objects.filter(id=review_id).exists()
        assert not Reply.objects.filter(review_id=review_id).exists()
        
        # Проверяем, что пользователи остались
        assert User.objects.filter(id=student.id).exists()
        assert User.objects.filter(id=teacher_user.id).exists()
        assert User.objects.filter(id=producer_user.id).exists()
    
    def test_specialization_teacher_dependency(self, teacher_user):
        """
        Тест зависимости между Specialization и TeacherProfile:
        - При удалении специализации она должна удаляться у всех учителей
        - При удалении учителя его специализации должны остаться
        """
        profile = TeacherProfile.objects.create(
            user=teacher_user,
            slug=get_unique_slug()
        )
        
        spec = Specialization.objects.create(
            name='Математика',
            description='Высшая математика',
            slug=get_unique_slug()
        )
        
        profile.specializations.add(spec)
        assert profile.specializations.count() == 1
        
        # При удалении специализации она должна удалиться у учителя
        spec_id = spec.id
        spec.delete()
        assert not profile.specializations.filter(id=spec_id).exists()
        
        # Создаем новую специализацию
        new_spec = Specialization.objects.create(
            name='Физика',
            description='Общая физика',
            slug=get_unique_slug()
        )
        profile.specializations.add(new_spec)
        
        # При удалении учителя специализация должна остаться
        spec_id = new_spec.id
        profile.delete()
        assert Specialization.objects.filter(id=spec_id).exists()
