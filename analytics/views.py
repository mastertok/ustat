from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import CourseView, LessonProgress, Revenue
from .serializers import CourseViewSerializer, LessonProgressSerializer, RevenueSerializer

# Create your views here.

class CourseViewViewSet(viewsets.ModelViewSet):
    queryset = CourseView.objects.all()
    serializer_class = CourseViewSerializer
    permission_classes = [permissions.IsAuthenticated]

class LessonProgressViewSet(viewsets.ModelViewSet):
    queryset = LessonProgress.objects.all()
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

class RevenueViewSet(viewsets.ModelViewSet):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    permission_classes = [permissions.IsAuthenticated]
