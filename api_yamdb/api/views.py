from django.conf import settings
from django.db.models import Avg
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import  viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from api.filters import TitleFilter
from api.mixins import CreateDestroyListViewSet
from api.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminOrReadOnly,
    IsAdmin,
)
from api.serializers import (
    CategorySerializer,
    CommentsSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
)
from reviews.models import Category, Genre, Review, Title

class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для моделей Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"

class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для моделей Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"

class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для Произведению."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleReadSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
    
class CommentViewSet(viewsets.ModelViewSet):
    """"Вьюсет для комментариев."""

    serializer_class = CommentsSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
