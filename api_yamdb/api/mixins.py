from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly


class CreateDestroyListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    """Базовый вьюсет для моделей Genre и Category."""
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class NotPutModelViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей с запретом PUT-запросов."""
    def update(self, request, *args, **kwargs):
        """PUT-запросы запрещены."""
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
