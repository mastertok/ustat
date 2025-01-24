"""
URL configuration for ustat project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API документация
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('api/accounts/', include('accounts.api.urls')),
    path('api/courses/', include('courses.api.urls')),
    path('api/reviews/', include('reviews.api.urls')),
    path('api/analytics/', include('analytics.api.urls')),
    
    # App URLs
    path('', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('reviews/', include('reviews.urls')),
    path('analytics/', include('analytics.urls')),
    
    # Профили преподавателей
    path('teacher/', include('accounts.teacher_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
