from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api.filters import TitleFilter
from api.mixins import CreateDestroyListViewSet
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorModeratorAdminOrReadonly)
from api.serializers import (AuthGetTokenSerializer, CategorySerializer,
                             CommentsSerializer, GenreSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             UserMePatchSerializer, UserSerializer)


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для моделей Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для моделей Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей Title."""
    queryset = Title.objects.annotate(rating=Avg('review__score'))
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей Review."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadonly)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей Comment."""
    serializer_class = CommentsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadonly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class AuthViewSet(viewsets.GenericViewSet):
    """Вьюсет для регистрации пользователей и получения токена."""
    from ._confirmation_code_utils import (generate_confirmation_code,
                                           send_user_confirmation_code)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'], name='Get token')
    def token(self, request):
        serializer = AuthGetTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.validated_data,
                            status=status.HTTP_200_OK)

        status_code = status.HTTP_400_BAD_REQUEST
        if request.data.get('username') and 'username' in serializer.errors:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(serializer.errors,
                        status=status_code)

    @action(detail=False, methods=['POST'], name='SignUp')
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(
                confirmation_code=self.generate_confirmation_code())
            self.send_user_confirmation_code(user)
            return Response(data=serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями и профилем пользователя."""
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['GET', 'PATCH'], name='User profile',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = UserMePatchSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
