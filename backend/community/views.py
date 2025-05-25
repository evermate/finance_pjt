from rest_framework import viewsets, permissions, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']

    # 조회수 증가 처리
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # ✅ 삭제 등 상세 조회에는 전체 queryset 허용
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return Comment.objects.all()
        queryset = Comment.objects.filter(parent=None).order_by('created_at')  # 부모만
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
