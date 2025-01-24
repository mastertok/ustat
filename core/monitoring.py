from prometheus_client import Counter, Histogram, Gauge
from functools import wraps
import time
from typing import Callable
from django.db import connection
from django.conf import settings
import logging

# Настройка логгера
logger = logging.getLogger(__name__)

# Метрики Prometheus
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)

active_users_total = Gauge(
    'active_users_total',
    'Total number of active users'
)

cache_hits_total = Counter(
    'cache_hits_total',
    'Total number of cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total number of cache misses',
    ['cache_type']
)

def monitor_view(view_func: Callable) -> Callable:
    """
    Декоратор для мониторинга view функций
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        method = request.method.lower()
        endpoint = request.path
        
        # Начало измерения времени
        start_time = time.time()
        
        try:
            response = view_func(request, *args, **kwargs)
            status = response.status_code
            
        except Exception as e:
            logger.exception(f"Error in view {view_func.__name__}: {str(e)}")
            status = 500
            raise
            
        finally:
            # Записываем метрики
            duration = time.time() - start_time
            http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
            http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
            
        return response
    return wrapper


def monitor_db_query(func: Callable) -> Callable:
    """
    Декоратор для мониторинга запросов к базе данных
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            # Определяем тип запроса
            query_type = 'unknown'
            if hasattr(args[0], 'query'):
                query = str(args[0].query).lower()
                if 'select' in query:
                    query_type = 'select'
                elif 'insert' in query:
                    query_type = 'insert'
                elif 'update' in query:
                    query_type = 'update'
                elif 'delete' in query:
                    query_type = 'delete'
            
            # Записываем метрики
            duration = time.time() - start_time
            db_query_duration_seconds.labels(query_type=query_type).observe(duration)
            
            # Логируем медленные запросы
            if duration > settings.SLOW_QUERY_THRESHOLD:
                logger.warning(f"Slow query detected: {query_type} took {duration:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.exception(f"Database query error: {str(e)}")
            raise
            
    return wrapper


def update_active_users_metric(count: int):
    """
    Обновление метрики активных пользователей
    """
    active_users_total.set(count)


def monitor_cache(func: Callable) -> Callable:
    """
    Декоратор для мониторинга кэша
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_type = kwargs.get('cache_type', 'default')
        
        try:
            result = func(*args, **kwargs)
            
            if result is not None:
                cache_hits_total.labels(cache_type=cache_type).inc()
            else:
                cache_misses_total.labels(cache_type=cache_type).inc()
                
            return result
            
        except Exception as e:
            logger.exception(f"Cache error: {str(e)}")
            raise
            
    return wrapper


class QueryCountMiddleware:
    """
    Middleware для подсчета количества SQL запросов
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Очищаем счетчики перед запросом
        initial_queries = len(connection.queries)
        
        response = self.get_response(request)
        
        # Подсчитываем количество запросов
        final_queries = len(connection.queries)
        num_queries = final_queries - initial_queries
        
        # Добавляем информацию в заголовки ответа
        response['X-Query-Count'] = str(num_queries)
        
        # Логируем большое количество запросов
        if num_queries > settings.MAX_QUERIES_WARNING:
            logger.warning(f"High number of queries detected: {num_queries} queries for {request.path}")
            
        return response
