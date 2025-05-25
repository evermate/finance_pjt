from django.db import models
from django.conf import settings

class Post(models.Model):
    BOARD_CHOICES = [
        ('REVIEW', '금융상품 리뷰'),
        ('NEWS', '금융 뉴스'),
        ('FREE', '자유 게시판'),
    ]
    board_type = models.CharField(max_length=10, choices=BOARD_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(blank=True)  # 뉴스용 (REVIEW/NEWS만 사용 가능)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 리뷰용 (1~5점)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    views = models.PositiveIntegerField(default=0)  # 조회수 필드 추가

    def __str__(self):
        return f"[{self.get_board_type_display()}] {self.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}의 댓글: {self.content[:20]}"
