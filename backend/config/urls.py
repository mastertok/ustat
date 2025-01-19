from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from apps.courses.views import CourseViewSet
from apps.partners.views import PartnerViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'partners', PartnerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/courses/', include('apps.courses.urls')),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
