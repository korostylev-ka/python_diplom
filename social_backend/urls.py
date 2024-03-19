"""
URL configuration for social_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import PostViewSet, redirect_to_api, \
    MakePostLikeAPIView, LikesListAPIView, CreateCommentAPIView, EditCommentUpdateAPIView, CommentDeleteAPIView

router_posts = DefaultRouter()
router_posts.register('posts', PostViewSet)
# router_comments = DefaultRouter()
# router_comments.register('comments', CommentViewSet)

urlpatterns = [
    path('', redirect_to_api),
    path('admin/', admin.site.urls),
    path('api/', include(router_posts.urls)),
    # path('api/posts/likes/<int:post_id>/', PostLikesAPIVIEW.as_view()),
    path('api/posts/like/<int:post_id>/', MakePostLikeAPIView.as_view()),
    path('api/likes/', LikesListAPIView.as_view()),
    path('api/posts/comment/<int:post_id>/', CreateCommentAPIView.as_view()),
    path('api/comments/update/<int:pk>/', EditCommentUpdateAPIView.as_view()),
    path('api/comments/delete/<int:pk>/', CommentDeleteAPIView.as_view()),
    # path('api/', include(router_comments.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
