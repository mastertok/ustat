from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'course-views', views.CourseViewViewSet)
router.register(r'lesson-progress', views.LessonProgressViewSet)
router.register(r'revenue', views.RevenueViewSet)

app_name = 'analytics'

urlpatterns = [
    path('api/', include(router.urls)),
]
