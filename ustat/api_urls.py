from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# API URLs
urlpatterns = [
    # API документация
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API endpoints
    path('accounts/', include('accounts.api.urls')),
    path('courses/', include('courses.api.urls')),
    path('reviews/', include('reviews.api.urls')),
]
