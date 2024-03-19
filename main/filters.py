from django_filters import DateTimeFromToRangeFilter
from django_filters import rest_framework as filters
from main.models import Post

class PostFilter(filters.FilterSet):
    """Фильтры для постов."""
    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['created_at', 'author']
