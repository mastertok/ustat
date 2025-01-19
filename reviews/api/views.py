from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from reviews.models import Review, Reply
from .serializers import ReviewSerializer, ReplySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'course_slug' in self.kwargs:
            return Review.objects.filter(course__slug=self.kwargs['course_slug'])
        return Review.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'review_id' in self.kwargs:
            return Reply.objects.filter(review_id=self.kwargs['review_id'])
        return Reply.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
