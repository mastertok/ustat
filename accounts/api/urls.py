from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('specializations', views.SpecializationViewSet)
router.register('teachers', views.TeacherProfileViewSet)
router.register('producers', views.ProducerProfileViewSet)
router.register('achievements', views.AchievementViewSet)
router.register('education', views.EducationViewSet)
router.register('work-experience', views.WorkExperienceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
