from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile, Achievement, Education, WorkExperience, Specialization

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ('role',)

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        exclude = ('profile',)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('profile',)

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        exclude = ('profile',)

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specializations = SpecializationSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True, source='achievement_records')
    education = EducationSerializer(many=True, read_only=True, source='education_records')
    work_experience = WorkExperienceSerializer(many=True, read_only=True, source='work_experiences')
    rating = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'specializations', 'achievements', 'education', 
                 'work_experience', 'rating', 'social_links', 'slug', 'created_at', 
                 'updated_at')
