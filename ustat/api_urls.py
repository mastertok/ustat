from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Устат API",
        default_version='v1',
        description="API для образовательной платформы Устат",
        terms_of_service="https://www.ustat.kg/terms/",
        contact=openapi.Contact(email="contact@ustat.kg"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API URLs
urlpatterns = [
    # API документация
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API endpoints
    path('accounts/', include('accounts.api.urls')),
    path('courses/', include('courses.api.urls')),
    path('reviews/', include('reviews.api.urls')),
]
