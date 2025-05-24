from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'board_type', 'title', 'content', 'link', 'rating',
            'author', 'created_at'
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'parent', 'created_at', 'children']
        read_only_fields = ['author', 'created_at']

    def get_children(self, obj):
        queryset = obj.children.all().order_by('created_at')
        return CommentSerializer(queryset, many=True).data

    def validate(self, data):
        parent = data.get('parent')
        if parent and parent.parent:
            raise serializers.ValidationError("대댓글의 대댓글은 허용되지 않습니다.")
        return data
