import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.models import ProducerProfile
from courses.models import Course, Category
from courses.models import Promocode, Promotion, CourseAnalytics, TrafficSource, EmailCampaign

User = get_user_model()

@pytest.fixture
def producer_with_profile(db):
    user = User.objects.create_user(
        username='producer1',
        password='testpass123',
        email='producer@test.com',
        role='producer'
    )
    profile = ProducerProfile.objects.create(
        user=user,
        company='Test Company'
    )
    return profile

@pytest.fixture
def course_with_analytics(producer_with_profile):
    category = Category.objects.create(
        name='Test Category',
        slug='test-category'
    )
    course = Course.objects.create(
        title='Test Course',
        slug='test-course',
        description='Test Description',
        category=category,
        producer=producer_with_profile,
        price=100.00,
        status='published',
        teacher=None
    )
    analytics = CourseAnalytics.objects.create(course=course)
    return course, analytics

@pytest.mark.django_db
class TestPromocode:
    def test_create_promocode(self, producer_with_profile, course_with_analytics):
        course, _ = course_with_analytics
        promocode = Promocode.objects.create(
            code='TEST20',
            discount_percent=20,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=30),
            max_uses=100,
            created_by=producer_with_profile
        )
        promocode.courses.add(course)
        
        assert promocode.code == 'TEST20'
        assert promocode.discount_percent == 20
        assert promocode.used_count == 0
        assert course in promocode.courses.all()
    
    def test_promocode_validation(self, producer_with_profile):
        # Тест на некорректный процент скидки
        with pytest.raises(ValidationError):
            promocode = Promocode(
                code='TEST120',
                discount_percent=120,  # Больше 100%
                valid_from=timezone.now(),
                valid_until=timezone.now() + timedelta(days=30),
                max_uses=100,
                created_by=producer_with_profile
            )
            promocode.full_clean()

@pytest.mark.django_db
class TestPromotion:
    def test_create_promotion(self, producer_with_profile, course_with_analytics):
        course, _ = course_with_analytics
        promotion = Promotion.objects.create(
            title='Summer Sale',
            description='Summer discount 30%',
            discount_percent=30,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            created_by=producer_with_profile
        )
        promotion.courses.add(course)
        
        assert promotion.title == 'Summer Sale'
        assert promotion.discount_percent == 30
        assert course in promotion.courses.all()

@pytest.mark.django_db
class TestCourseAnalytics:
    def test_analytics_creation(self, course_with_analytics):
        course, analytics = course_with_analytics
        
        assert analytics.views_count == 0
        assert analytics.cart_adds_count == 0
        assert analytics.purchases_count == 0
    
    def test_increment_analytics(self, course_with_analytics):
        _, analytics = course_with_analytics
        
        analytics.views_count += 1
        analytics.cart_adds_count += 1
        analytics.save()
        
        assert analytics.views_count == 1
        assert analytics.cart_adds_count == 1

@pytest.mark.django_db
class TestTrafficSource:
    def test_create_traffic_source(self, course_with_analytics):
        course, _ = course_with_analytics
        traffic = TrafficSource.objects.create(
            course=course,
            source='facebook',
            utm_campaign='summer_campaign',
            utm_content='banner_1'
        )
        
        assert traffic.source == 'facebook'
        assert traffic.views_count == 0
        assert traffic.conversion_count == 0
    
    def test_track_traffic(self, course_with_analytics):
        course, _ = course_with_analytics
        traffic = TrafficSource.objects.create(
            course=course,
            source='instagram'
        )
        
        traffic.views_count += 1
        traffic.conversion_count += 1
        traffic.save()
        
        assert traffic.views_count == 1
        assert traffic.conversion_count == 1

@pytest.mark.django_db
class TestEmailCampaign:
    def test_create_campaign(self, producer_with_profile, course_with_analytics):
        course, _ = course_with_analytics
        campaign = EmailCampaign.objects.create(
            title='Welcome Campaign',
            subject='Welcome to our course!',
            content='Thank you for joining...',
            created_by=producer_with_profile
        )
        campaign.courses.add(course)
        
        assert campaign.title == 'Welcome Campaign'
        assert campaign.recipients_count == 0
        assert campaign.opens_count == 0
        assert campaign.clicks_count == 0
        assert course in campaign.courses.all()
    
    def test_campaign_metrics(self, producer_with_profile, course_with_analytics):
        course, _ = course_with_analytics
        campaign = EmailCampaign.objects.create(
            title='Test Campaign',
            subject='Test Subject',
            content='Test Content',
            created_by=producer_with_profile
        )
        
        # Симулируем отправку и метрики
        campaign.sent_at = timezone.now()
        campaign.recipients_count = 100
        campaign.opens_count = 50
        campaign.clicks_count = 25
        campaign.save()
        
        assert campaign.recipients_count == 100
        assert campaign.opens_count == 50
        assert campaign.clicks_count == 25
