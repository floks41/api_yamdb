"""Модуль представлений для приложения Users проекта API_Yamdb."""


from api.permissions import IsAdmin
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import (UserMeSerializer,
                               UserSerializer, SignUpSerializer, AuthGetTokenSerializer)


class AuthViewSet(viewsets.GenericViewSet):
    from ._send_confirmation_code import send_user_confirmation_code
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'], name='get token')
    def token(self, request, *args, **kwargs):
        serializer = AuthGetTokenSerializer(data=request.data)
        if serializer.is_valid():

            return Response(data=serializer.validated_data,
                            status=status.HTTP_200_OK)
        print(serializer.errors)
        status_code = status.HTTP_400_BAD_REQUEST
        if request.data.get('username') and 'username' in serializer.errors:
            status_code = status.HTTP_404_NOT_FOUND
            return Response(status=status_code)
        return Response(serializer.errors,
                        status=status_code)

    @action(detail=False, methods=['POST'], name='get token')
    def signup(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(confirmation_code=BaseUserManager.make_random_password(None))
            self.send_user_confirmation_code(user)
            return Response(data=serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)



class AuthGetTokenView2(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        
        serializer = AuthGetTokenSerializer(data=request.data)
        if serializer.is_valid():

            return Response(data=serializer.validated_data,
                            status=status.HTTP_200_OK)
        print(serializer.errors)
        status_code = status.HTTP_400_BAD_REQUEST
        if request.data.get('username') and 'username' in serializer.errors:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(serializer.errors,
                        status=status_code)


class AuthSignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(confirmation_code=BaseUserManager.make_random_password(None))
            
            send_mail(subject="Confirmation code",
                  message=user.confirmation_code,
                  from_email="admin@yamdb.fun",
                  recipient_list=[user.email, ])
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
        
    @action(detail=False, methods=['GET', 'PATCH'], name='User profile',
            permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = UserMeSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
