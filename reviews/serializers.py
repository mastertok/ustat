from rest_framework import serializers
from .models import Review, Reply
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Reply
        fields = ('id', 'user', 'review', 'content', 'created_at')
        read_only_fields = ('user',)

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'course', 'rating', 'content', 'created_at', 
                 'replies', 'likes_count', 'user_has_liked')
        read_only_fields = ('user',)
        
    def get_likes_count(self, obj):
        return obj.likes.count()
        
    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False
