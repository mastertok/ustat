from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'courses/(?P<course_slug>[\w-]+)/reviews', views.ReviewViewSet)
router.register(r'reviews/(?P<review_id>\d+)/replies', views.ReplyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
