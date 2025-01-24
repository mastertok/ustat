from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet)
router.register(r'replies', views.ReplyViewSet)

app_name = 'reviews'

urlpatterns = [
    path('api/', include(router.urls)),
]
