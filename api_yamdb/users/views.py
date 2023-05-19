"""Модуль представлений для приложения Users проекта API_Yamdb."""


from api.permissions import IsAdmin
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.serializers import (AuthGetTokenSerializer, SignUpSerializer,
                               UserMePatchSerializer, UserSerializer)


class AuthViewSet(viewsets.GenericViewSet):
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
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        """PUT-method is prohibited."""
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

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
