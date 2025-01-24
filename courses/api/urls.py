from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('tags', views.TagViewSet, basename='tag')
router.register('courses', views.CourseViewSet, basename='course')
router.register(r'courses/(?P<course_slug>[\w-]+)/modules', views.ModuleViewSet, basename='course-module')
router.register(r'modules/(?P<module_id>\d+)/lessons', views.LessonViewSet, basename='module-lesson')
router.register(r'courses/(?P<course_slug>[\w-]+)/announcements', views.AnnouncementViewSet, basename='course-announcement')

urlpatterns = [
    path('', include(router.urls)),
]
