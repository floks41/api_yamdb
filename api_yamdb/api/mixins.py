from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class CreateDestroyListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class NotPutModelViewSet(viewsets.ModelViewSet):

    def update(self, request, *args, **kwargs):
        """PUT-method is prohibited."""
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
