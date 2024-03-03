from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from main.models import Post, Like
from main.serializers import PostSerializer, LikeSerializer


# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


