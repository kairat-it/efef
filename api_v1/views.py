from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from webapp.models import Post
from .permissions import IsAuthor
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['create', 'like', 'unlike']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated(), IsAuthor()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.like_users.all():
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        post.like_users.add(request.user)
        return Response({'status': 'post liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user not in post.like_users.all():
            return Response({'detail': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)
        post.like_users.remove(request.user)
        return Response({'status': 'post unliked'})