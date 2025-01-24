from rest_framework import serializers
from .models import CourseView, LessonProgress, Revenue

class CourseViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseView
        fields = '__all__'

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'
