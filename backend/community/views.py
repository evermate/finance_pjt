from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer

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
