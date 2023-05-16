from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentsViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitlesViewSet,
)


class NoPutRouter(routers.DefaultRouter):
    """Класс роутер, отключающий PUT запросы."""

    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        if 'put' in bound_methods.keys():
            del bound_methods['put']
        return bound_methods


router_v1 = NoPutRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments',
)

