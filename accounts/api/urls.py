from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('profiles', views.ProfileViewSet, basename='profile')
router.register('education', views.EducationViewSet, basename='education')
router.register('work-experience', views.WorkExperienceViewSet, basename='work-experience')
router.register('achievements', views.AchievementViewSet, basename='achievement')

app_name = 'accounts-api'

urlpatterns = [
    path('teachers/check-url/', views.check_custom_url_availability, name='check-custom-url'),
    path('', include(router.urls)),
]
