from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title
from api.filters import TitleFilter
from api.mixins import CreateDestroyListViewSet

from api.permissions import IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadonly
from api.serializers import (CategorySerializer, CommentsSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для моделей Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для моделей Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('review__score'))
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
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

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadonly,
    )

    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentsSerializer

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadonly,)


    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
