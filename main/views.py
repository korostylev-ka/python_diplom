import urllib
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from main.filters import PostFilter
from main.models import Post, Like, Comment
from main.permissions import IsOwnerOrReadOnly
from main.serializers import PostSerializer, LikeSerializer, CommentSerializer, LikesListSerializer


# Create your views here.
def redirect_to_api(request):
    response = redirect('/api/')
    return response


class PostViewSet(ModelViewSet):
    """ViewSet для постов."""
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostFilter

    # Сохраняем изображение из url в Imagefield
    def perform_update(self, serializer):
        instance = self.get_object()
        url = self.request.data.get("image", None)
        image_file = ''
        if url != None:
            try:
                response = urllib.request.urlopen(url)
                image_data = response.read()
                image_file = ContentFile(image_data, name="post_image.jpg")
            except:
                image_file = None
        if serializer.is_valid(raise_exception=True):
            post_save = serializer.save(author=self.request.user, image=image_file)
            return Response('Пост успешно обновлен')

   # Обновление Imagefield по url
    def perform_create(self, serializer):
        post = self.request.data
        print(post)
        url = post.get('image')
        image_file = ''
        if url != None:
            try:
                response = urllib.request.urlopen(url)
                image_data = response.read()
                image_file = ContentFile(image_data, name="post_image.jpg")
            except:
                image_file = None
        else:
            image_file = None
        serializer.save(author=self.request.user, image=image_file)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

class PostLikesAPIView(APIView):
    """ViewSet для просмотра лайка"""

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, post_id):
        like = Like.objects.filter(post_id=post_id)
        ser = LikeSerializer(like, many=True)
        return Response(ser.data)


class MakePostLikeAPIView(APIView):
    """ViewSet для лайка/дизлайка"""

    def post(self, request, post_id):
        # is_liked = Like.objects.all().filter(user=self.request.user.id, post=request.data['post'])
        is_liked = Like.objects.all().filter(user=self.request.user.id, post=post_id)
        print(is_liked)
        if is_liked.count() == 0:
            like = request.data
            like['post'] = post_id
            serializer = LikeSerializer(data=like)
            if serializer.is_valid(raise_exception=True):  # если данные валидны
                liked = serializer.save(user=request.user)
                return Response('Лайк поставлен')
        else:
            is_liked.delete()
            return Response('Дизлайк')

class LikesListAPIView(ListAPIView):
    """ViewSet для списка лайков по постам"""
    queryset = Post.objects.all().exclude(likes=None).order_by('id')
    # serializer_class = LikeSerializer
    serializer_class = LikesListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # serializer = LikeSerializer(queryset, many=True)
        serializer = LikesListSerializer(queryset, many=True)
        return Response(serializer.data)


class CreateCommentAPIView(APIView):
    """ViewSet для создания комментария"""

    def post(self, request, post_id):
        comment = request.data
        try:
            post = Post.objects.all().filter(id=post_id)[0]
            serializer = CommentSerializer(data=comment)
            if serializer.is_valid(raise_exception=True):  # если данные валидны
                comment_saved = serializer.save(author=request.user, post=post)
                return Response('Комментарий оставлен')
        except:
            return Response('Неверный пост')

class EditCommentUpdateAPIView(UpdateAPIView):
    """ViewSet для редактирования комментария"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Комментарий успешно изменен')
        else:
            return request

class CommentDeleteAPIView(DestroyAPIView):
    """ViewSet для удаления комментария"""

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
