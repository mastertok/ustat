import pytest
from django.test import TestCase
from django.db import connection
from django.db.models import Q
from accounts.models import User, Profile, Specialization, Education, WorkExperience, Achievement

class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='teacher'
        )

    def test_role_username_index(self):
        """Проверяем, что составной индекс role+username используется при фильтрации"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'accounts_user'
            """)
            indexes = cursor.fetchall()
            assert any('role' in idx[1] and 'username' in idx[1] for idx in indexes)

    def test_active_users_partial_index(self):
        """Проверяем, что частичный индекс для активных пользователей работает"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'accounts_user' 
                AND indexdef LIKE '%WHERE is_active%'
            """)
            assert cursor.fetchone() is not None

    def test_role_permissions(self):
        """Проверяем корректность возвращаемых разрешений для разных ролей"""
        # Учитель
        self.user.role = 'teacher'
        permissions = self.user.get_role_permissions()
        assert 'can_create_course' in permissions
        assert 'can_edit_own_course' in permissions

        # Студент
        self.user.role = 'student'
        permissions = self.user.get_role_permissions()
        assert 'can_enroll_course' in permissions
        assert 'can_leave_review' in permissions

        # Продюсер
        self.user.role = 'producer'
        permissions = self.user.get_role_permissions()
        assert 'can_edit_course_landing' in permissions
        assert 'can_manage_promotions' in permissions

class TestProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            rating=4.5,
            social_links={'twitter': '@test'},
            role_data={}
        )

    def test_profile_indexes(self):
        """Проверяем наличие индексов в таблице профилей"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'accounts_profile'
            """)
            indexes = cursor.fetchall()
            assert any('user_id' in idx[1] and 'rating' in idx[1] for idx in indexes)
            assert any('slug' in idx[1] for idx in indexes)

    def test_slug_generation(self):
        """Проверяем автоматическую генерацию slug"""
        self.assertEqual(
            self.profile.slug,
            f"{self.user.username}-{self.user.role}"
        )

    def test_role_specific_data(self):
        """Проверяем работу с данными специфичными для роли"""
        test_data = {'experience_years': 5}
        self.profile.set_role_data(test_data)
        self.assertEqual(
            self.profile.role_specific_data,
            test_data
        )

class TestSpecializationModel(TestCase):
    def setUp(self):
        self.specialization = Specialization.objects.create(
            name='Python Development',
            description='Python programming and web development'
        )

    def test_specialization_indexes(self):
        """Проверяем наличие составного индекса name+slug"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'accounts_specialization'
            """)
            indexes = cursor.fetchall()
            assert any('name' in idx[1] and 'slug' in idx[1] for idx in indexes)

    def test_slug_auto_generation(self):
        """Проверяем автоматическую генерацию slug"""
        self.assertEqual(
            self.specialization.slug,
            'python-development'
        )

class TestEducationModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            rating=4.5
        )
        self.education = Education.objects.create(
            profile=self.profile,
            institution='Test University',
            degree='Bachelor',
            field_of_study='Computer Science',
            start_date='2020-01-01',
            end_date='2024-01-01'
        )

    def test_education_indexes(self):
        """Проверяем наличие индексов для дат"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'accounts_education'
            """)
            indexes = cursor.fetchall()
            assert any('profile_id' in idx[1] and 'start_date' in idx[1] for idx in indexes)
            assert any('profile_id' in idx[1] and 'end_date' in idx[1] for idx in indexes)

class TestWorkExperienceModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            rating=4.5
        )
        self.experience = WorkExperience.objects.create(
            profile=self.profile,
            company='Test Company',
            position='Developer',
            start_date='2020-01-01',
            is_current=True
        )

    def test_work_experience_indexes(self):
        """Проверяем наличие индексов"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'accounts_workexperience'
            """)
            indexes = cursor.fetchall()
            assert any('profile_id' in idx[1] and 'is_current' in idx[1] for idx in indexes)
            assert any('profile_id' in idx[1] and 'start_date' in idx[1] for idx in indexes)

    def test_current_job_handling(self):
        """Проверяем, что у текущей работы end_date всегда None"""
        self.assertIsNone(self.experience.end_date)
        
        # Меняем is_current на False
        self.experience.is_current = False
        self.experience.end_date = '2024-01-01'
        self.experience.save()
        self.assertIsNotNone(self.experience.end_date)

class TestAchievementModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            rating=4.5
        )
        self.achievement = Achievement.objects.create(
            profile=self.profile,
            title='Test Certificate',
            date_received='2024-01-01',
            issuer='Test Institute'
        )

    def test_achievement_indexes(self):
        """Проверяем наличие индекса для даты получения"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'accounts_achievement'
            """)
            indexes = cursor.fetchall()
            assert any('profile_id' in idx[1] and 'date_received' in idx[1] for idx in indexes)
