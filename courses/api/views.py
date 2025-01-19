from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from courses.models import Course, Module, Lesson, Announcement, Category, Tag
from .serializers import (
    CourseSerializer, CourseListSerializer, ModuleSerializer,
    LessonSerializer, AnnouncementSerializer, CategorySerializer,
    TagSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tags', 'difficulty_level', 'language', 'course_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'published_at', 'price']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        if self.action == 'list':
            queryset = queryset.filter(status='published')
        return queryset

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'course_slug' in self.kwargs:
            return Module.objects.filter(course__slug=self.kwargs['course_slug'])
        return Module.objects.none()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'module_id' in self.kwargs:
            return Lesson.objects.filter(module_id=self.kwargs['module_id'])
        return Lesson.objects.none()

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'course_slug' in self.kwargs:
            return Announcement.objects.filter(course__slug=self.kwargs['course_slug'])
        return Announcement.objects.none()
