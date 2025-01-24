from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.cache import cache
from django.conf import settings
from functools import wraps
from typing import Type, Optional
from django.db.models import QuerySet

class StandardResultsSetPagination(PageNumberPagination):
    """
    Стандартная пагинация для всех API эндпоинтов
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BaseThrottle:
    """
    Базовые ограничения запросов к API
    """
    class BurstRateThrottle(UserRateThrottle):
        scope = 'burst'
        rate = '60/min'  # 60 запросов в минуту

    class SustainedRateThrottle(UserRateThrottle):
        scope = 'sustained'
        rate = '1000/day'  # 1000 запросов в день

    class AnonBurstRateThrottle(AnonRateThrottle):
        scope = 'anon_burst'
        rate = '30/min'  # 30 запросов в минуту для анонимных пользователей


def cache_response(timeout: int = 300, key_prefix: str = ''):
    """
    Декоратор для кэширования ответов API
    
    Args:
        timeout (int): Время жизни кэша в секундах
        key_prefix (str): Префикс для ключа кэша
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(view_instance, request, *args, **kwargs):
            # Формируем ключ кэша
            cache_key = f"{key_prefix}:{request.path}:{request.query_params}"
            
            # Проверяем наличие данных в кэше
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # Если данных нет в кэше, выполняем запрос
            response = view_func(view_instance, request, *args, **kwargs)
            
            # Сохраняем результат в кэш
            cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator


class BaseViewSet(GenericViewSet):
    """
    Базовый ViewSet с общей функциональностью для всех API эндпоинтов
    """
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    throttle_classes = [BaseThrottle.BurstRateThrottle, BaseThrottle.SustainedRateThrottle]
    
    def get_queryset(self) -> QuerySet:
        """
        Получение базового QuerySet с учетом кэширования
        """
        queryset = super().get_queryset()
        
        # Добавляем select_related и prefetch_related если они определены
        if hasattr(self, 'select_related_fields'):
            queryset = queryset.select_related(*self.select_related_fields)
        if hasattr(self, 'prefetch_related_fields'):
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
            
        return queryset
    
    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        """
        Фильтрация QuerySet с поддержкой сортировки и фильтров
        """
        # Применяем базовую фильтрацию
        queryset = super().filter_queryset(queryset)
        
        # Сортировка
        ordering = self.request.query_params.get('ordering')
        if ordering:
            order_fields = ordering.split(',')
            queryset = queryset.order_by(*order_fields)
            
        return queryset


class ReadOnlyViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """
    ViewSet только для чтения данных
    """
    pass


class ModelViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin):
    """
    Полный ViewSet для работы с моделями
    """
    pass


class CQRSViewSet(ModelViewSet):
    """
    ViewSet с поддержкой CQRS паттерна
    """
    command_serializer_class: Optional[Type] = None
    query_serializer_class: Optional[Type] = None
    
    def get_serializer_class(self):
        """
        Выбор сериализатора в зависимости от типа операции
        """
        if self.action in ['create', 'update', 'partial_update'] and self.command_serializer_class:
            return self.command_serializer_class
        if self.action in ['list', 'retrieve'] and self.query_serializer_class:
            return self.query_serializer_class
        return super().get_serializer_class()


from rest_framework import pagination, viewsets
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from typing import Any, Dict, Optional

class StandardResultsSetPagination(pagination.PageNumberPagination):
    """
    Стандартная пагинация для API
    """
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data: Any) -> Response:
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class CachedViewSetMixin:
    """
    Миксин для кэширования результатов API
    """
    cache_timeout: int = 60 * 15  # 15 минут по умолчанию
    
    def get_cache_key(self, **kwargs) -> str:
        """
        Генерирует ключ кэша для текущего запроса
        """
        return f"{self.__class__.__name__}:{self.action}:{self.request.query_params}"
    
    def get_cached_data(self, cache_key: str) -> Optional[Dict]:
        """
        Получает данные из кэша
        """
        return cache.get(cache_key)
    
    def set_cached_data(self, cache_key: str, data: Dict) -> None:
        """
        Сохраняет данные в кэш
        """
        cache.set(cache_key, data, self.cache_timeout)


class BaseViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet с общей функциональностью
    """
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_context(self) -> Dict:
        """
        Добавляет дополнительный контекст в сериализатор
        """
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        })
        return context
