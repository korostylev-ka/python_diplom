from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=1000, null=False, verbose_name='Текст поста')
    image = models.ImageField(upload_to='post_images', null=True, blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=1000, null=False, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
