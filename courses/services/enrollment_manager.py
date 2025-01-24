from django.db import transaction
from django.core.cache import cache
from django.utils import timezone
from courses.models import Course, Enrollment
from courses.services.analytics import CourseAnalyticsService

class EnrollmentManager:
    """Сервис для управления записями на курсы"""
    
    @staticmethod
    @transaction.atomic
    def enroll_student(course, student, payment_data=None):
        """Записывает студента на курс"""
        # Проверяем, не записан ли уже студент
        if Enrollment.objects.filter(course=course, student=student).exists():
            raise ValueError("Студент уже записан на этот курс")
            
        # Создаем запись
        enrollment = Enrollment.objects.create(
            course=course,
            student=student,
            status='active',
            payment_status='pending'
        )
        
        # Если есть данные об оплате, обрабатываем их
        if payment_data:
            enrollment = EnrollmentManager.process_payment(enrollment, payment_data)
            
        # Инвалидируем кеш статистики курса
        CourseAnalyticsService.invalidate_cache(course)
        
        return enrollment

    @staticmethod
    @transaction.atomic
    def process_payment(enrollment, payment_data):
        """Обрабатывает оплату за курс"""
        enrollment.payment_amount = payment_data['amount']
        enrollment.payment_method = payment_data['method']
        enrollment.payment_status = 'paid'
        enrollment.paid_at = timezone.now()
        enrollment.save()
        
        return enrollment

    @staticmethod
    def get_student_enrollments(student, status=None):
        """Получает все записи студента на курсы"""
        enrollments = Enrollment.objects.filter(
            student=student
        ).select_related(
            'course',
            'course__category'
        ).prefetch_related(
            'course__tags',
            'completed_lessons'
        )
        
        if status:
            enrollments = enrollments.filter(status=status)
            
        return enrollments

    @staticmethod
    @transaction.atomic
    def complete_lesson(enrollment, lesson):
        """Отмечает урок как завершенный"""
        enrollment.completed_lessons.add(lesson)
        enrollment.last_activity = timezone.now()
        enrollment.save()
        
        # Проверяем, завершен ли курс
        total_lessons = enrollment.course.get_total_lessons()
        completed_lessons = enrollment.completed_lessons.count()
        
        if total_lessons == completed_lessons:
            enrollment.status = 'completed'
            enrollment.completed_at = timezone.now()
            enrollment.save()
            
        # Инвалидируем кеш
        CourseAnalyticsService.invalidate_cache(enrollment.course)
        
        return enrollment

    @staticmethod
    @transaction.atomic
    def pause_enrollment(enrollment, reason=None):
        """Приостанавливает обучение"""
        enrollment.status = 'paused'
        enrollment.pause_reason = reason
        enrollment.paused_at = timezone.now()
        enrollment.save()
        
        return enrollment

    @staticmethod
    @transaction.atomic
    def resume_enrollment(enrollment):
        """Возобновляет обучение"""
        enrollment.status = 'active'
        enrollment.pause_reason = None
        enrollment.paused_at = None
        enrollment.save()
        
        return enrollment

    @staticmethod
    @transaction.atomic
    def cancel_enrollment(enrollment, reason=None):
        """Отменяет запись на курс"""
        enrollment.status = 'cancelled'
        enrollment.cancellation_reason = reason
        enrollment.cancelled_at = timezone.now()
        enrollment.save()
        
        # Инвалидируем кеш
        CourseAnalyticsService.invalidate_cache(enrollment.course)
        
        return enrollment

    @staticmethod
    def get_course_progress(enrollment):
        """Получает прогресс прохождения курса"""
        total_lessons = enrollment.course.get_total_lessons()
        if not total_lessons:
            return 0
            
        completed_lessons = enrollment.completed_lessons.count()
        return (completed_lessons / total_lessons) * 100

    @staticmethod
    def get_active_students_count(course):
        """Получает количество активных студентов на курсе"""
        cache_key = f'active_students_{course.id}'
        count = cache.get(cache_key)
        
        if count is None:
            count = course.enrollments.filter(status='active').count()
            cache.set(cache_key, count, 3600)  # кешируем на 1 час
            
        return count
