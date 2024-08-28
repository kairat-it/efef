from rest_framework import serializers
from webapp.models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'image', 'content', 'author', 'created_at', 'updated_at', 'likes_count']