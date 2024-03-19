from rest_framework import serializers
from rest_framework.authtoken.admin import User
from main.models import Post, Like, Comment


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = 'user'


class LikeSerializer(serializers.ModelSerializer):
    """Serializer для лайков."""
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Like
        fields = ('user', 'post')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для комментариев."""

    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_at')
        read_only_fields = ('author',)


class PostSerializer(serializers.ModelSerializer):
    """Serializer для постов."""

    comments = CommentSerializer(read_only=True, many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'image', 'created_at', 'comments', 'likes_count')
        read_only_fields = ('author', 'image')

    def get_likes_count(self, obj):
        likes = Like.objects.all()
        likes_count = likes.filter(post_id=obj.id)
        return likes_count.count()


class LikesListSerializer(serializers.ModelSerializer):
    """Serializer для списка лайков по постам."""

    users_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'users_liked')

    def get_users_liked(self, obj):
        users = []
        likes = Like.objects.all().filter(post=obj.id)
        for like in likes:
            users.append({'user': like.user.id})
        return users
