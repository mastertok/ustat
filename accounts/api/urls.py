from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('specializations', views.SpecializationViewSet, basename='specialization')
router.register('teachers', views.TeacherProfileViewSet, basename='teacher')
router.register('producers', views.ProducerProfileViewSet, basename='producer')
router.register('achievements', views.AchievementViewSet, basename='achievement')
router.register('education', views.EducationViewSet, basename='education')
router.register('work-experience', views.WorkExperienceViewSet, basename='work-experience')
router.register('profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
