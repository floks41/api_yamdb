from api.permissions import IsAdmin
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserSerializer


class UsersView(ListCreateAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination


class AuthGetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, username=username,
                                 confirmation_code=confirmation_code)
        token = RefreshToken.for_user(user)
        return Response(
            {
                'token': str(token.access_token),
            }
        )


class AuthSignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        user = get_object_or_404(User, username=username, email=email)
        confirmation_code = BaseUserManager.make_random_password(self)
        user.confirmation_code = confirmation_code
        user.save()
        print(request.user.is_superuser)
        send_mail(subject="Confirmation code",
                  message=confirmation_code,
                  from_email="admin@yamdb.fun",
                  recipient_list=[user.email, ])
        return Response(
            {
                'email': email,
                'username': username
            }
        )
