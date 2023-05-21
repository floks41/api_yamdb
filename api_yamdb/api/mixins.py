from rest_framework import mixins, viewsets


class CreateDestroyListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class NotPutViewSet(viewsets.GenericViewSet):

def update(self, request, *args, **kwargs):
    """PUT-method is prohibited."""
    if request.method == 'PUT':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().update(request, *args, **kwargs)
