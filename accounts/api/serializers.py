from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile, Education, WorkExperience, Achievement

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'is_verified')
        read_only_fields = ('role', 'is_verified')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'avatar', 'bio', 'language', 'social_links', 
                 'role_data', 'rating', 'courses_count', 'reviews_count', 
                 'verification_status', 'verified_at', 'created_at', 'updated_at')

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('user',)

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        read_only_fields = ('user',)

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
        read_only_fields = ('user',)
