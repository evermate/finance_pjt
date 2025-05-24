from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 쿼리파라미터 필터링
    def get_queryset(self):
        queryset = super().get_queryset()
        board_type = self.request.query_params.get('board_type')
        if board_type:
            queryset = queryset.filter(board_type=board_type)
        return queryset

    # 작성자 자동 저장
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes.add(request.user)
        return Response({'liked': True, 'like_count': post.likes.count()})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.likes.remove(request.user)
        return Response({'liked': False, 'like_count': post.likes.count()})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None).order_by('created_at')  # 부모만
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
