from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)
router.register('courses', views.CourseViewSet)
router.register(r'courses/(?P<course_slug>[\w-]+)/modules', views.ModuleViewSet)
router.register(r'modules/(?P<module_id>\d+)/lessons', views.LessonViewSet)
router.register(r'courses/(?P<course_slug>[\w-]+)/announcements', views.AnnouncementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
