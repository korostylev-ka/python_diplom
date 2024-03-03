from rest_framework import serializers

from main.models import Post, Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'is_liked', 'count')


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('text', 'likes')
