from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Category, Module, Lesson
from .serializers import (
    CourseSerializer, 
    CategorySerializer,
    ModuleSerializer,
    LessonSerializer
)
from .filters import CourseFilter
from .permissions import IsTeacherOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    """API endpoint для работы с курсами"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'excerpt']
    ordering_fields = [
        'price', 
        'created_at', 
        'average_rating',
        'students_count',
        'duration'
    ]
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Получение рекомендованных курсов"""
        queryset = self.get_queryset().filter(
            status='published',
            average_rating__gte=4.0
        ).order_by('-average_rating')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def price_ranges(self, request):
        """Получение диапазонов цен"""
        queryset = self.get_queryset()
        min_price = queryset.order_by('price').first().price
        max_price = queryset.order_by('-price').first().price
        return Response({
            'min_price': min_price,
            'max_price': max_price
        })

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint для работы с категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Получение курсов в категории"""
        category = self.get_object()
        courses = Course.objects.filter(
            category=category,
            status='published'
        )
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class ModuleViewSet(viewsets.ModelViewSet):
    """API endpoint для работы с модулями"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsTeacherOrReadOnly]
    
    def get_queryset(self):
        """Фильтрация модулей по курсу"""
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course', None)
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        return queryset

class LessonViewSet(viewsets.ModelViewSet):
    """API endpoint для работы с уроками"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrReadOnly]
    
    def get_queryset(self):
        """Фильтрация уроков по модулю"""
        queryset = super().get_queryset()
        module_id = self.request.query_params.get('module', None)
        if module_id is not None:
            queryset = queryset.filter(module_id=module_id)
        return queryset
