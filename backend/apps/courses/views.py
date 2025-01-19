from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Category, Review
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    CategorySerializer,
    ReviewSerializer
)


class IsEnrolledOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.students.filter(id=request.user.id).exists()


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_courses = self.get_queryset().order_by('-students_count')[:6]
        serializer = self.get_serializer(popular_courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        if course.favorites.filter(id=user.id).exists():
            course.favorites.remove(user)
            return Response({'status': 'removed from favorites'})
        else:
            course.favorites.add(user)
            return Response({'status': 'added to favorites'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        if course.students.filter(id=user.id).exists():
            return Response(
                {'error': 'Already enrolled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course.students.add(user)
        course.students_count = course.students.count()
        course.save()
        
        return Response({'status': 'enrolled'})

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated, IsEnrolledOrReadOnly]
    )
    def review(self, request, pk=None):
        course = self.get_object()
        serializer = ReviewSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        rating = self.request.query_params.get('rating__gte')
        if rating:
            queryset = queryset.filter(rating__gte=rating)
        return queryset.order_by('-created_at')
