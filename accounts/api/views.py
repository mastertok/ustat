from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from accounts.models import Profile, Achievement, Education, WorkExperience, Specialization
from .serializers import (
    UserSerializer, ProfileSerializer,
    AchievementSerializer, EducationSerializer, WorkExperienceSerializer,
    SpecializationSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(user__role=role)
        if 'specialization' in self.request.query_params:
            specialization = self.request.query_params['specialization']
            queryset = queryset.filter(specializations__slug=specialization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(user__role='teacher')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'specialization' in self.request.query_params:
            specialization = self.request.query_params['specialization']
            queryset = queryset.filter(specializations__slug=specialization)
        return queryset

class ProducerProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(user__role='producer')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkExperience.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
