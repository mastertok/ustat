from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from accounts.models import Profile, Education, WorkExperience, Achievement
from .serializers import (
    UserSerializer, ProfileSerializer, EducationSerializer,
    WorkExperienceSerializer, AchievementSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'custom_url'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(user__role='teacher', user__is_active=True)
        return queryset

    def perform_update(self, serializer):
        # Если обновляется custom_url, проверяем его доступность
        if 'custom_url' in serializer.validated_data:
            custom_url = serializer.validated_data['custom_url']
            if Profile.objects.filter(custom_url=custom_url).exclude(id=self.get_object().id).exists():
                raise serializers.ValidationError({'custom_url': 'Этот URL уже занят'})
        serializer.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(user__role=role)
        return queryset

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(user__role='teacher')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkExperience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AchievementViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_custom_url_availability(request):
    """
    Проверяет доступность URL для профиля преподавателя
    GET /api/teachers/check-url/?name=john-doe
    """
    custom_url = request.GET.get('name')
    if not custom_url:
        return Response({'error': 'Параметр name обязателен'}, status=status.HTTP_400_BAD_REQUEST)
    
    custom_url = slugify(custom_url)
    is_available = not Profile.objects.filter(custom_url=custom_url).exists()
    
    return Response({
        'custom_url': custom_url,
        'is_available': is_available
    })
