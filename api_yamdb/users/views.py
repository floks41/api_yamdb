from api.permissions import IsAdmin
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import (UserAuthSignUpSerializer, UserMeSerializer,
                               UserSerializer)


class AuthGetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not request.data or not username:
            return Response('No request data.',
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            return Response('Wrong username.',
                            status=status.HTTP_404_NOT_FOUND)
        if user.confirmation_code != confirmation_code:
            return Response('Wrong confirmation_code.',
                            status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response(
            {
                'token': str(token.access_token),
            },
            status=status.HTTP_200_OK
        )


class AuthSignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email', '')
        username = request.data.get('username', '')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                return Response('Wrong email.',
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = UserAuthSignUpSerializer(data=request.data)
        else:
            serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')

        user, created = User.objects.get_or_create(
            username=username, email=email)
        confirmation_code = BaseUserManager.make_random_password(self)

        user.confirmation_code = confirmation_code
        user.save()

        send_mail(subject="Confirmation code",
                  message=confirmation_code,
                  from_email="admin@yamdb.fun",
                  recipient_list=[user.email, ])
        return Response(data=serializer.validated_data,
                        status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['GET', 'PATCH'], name='User profile',
            permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserMeSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserMeSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
