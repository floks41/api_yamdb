from django.urls import path, include
from users.views import UsersView, AuthGetTokenView, AuthSignUpView

app_name = 'api'

urlpatterns = []

# Эндпоинты работы с пользователями авторизации и регистрации
urlpatterns += [
    path('users/', UsersView.as_view()),
    path('auth/token/', AuthGetTokenView.as_view()),
    path('auth/signup/', AuthSignUpView.as_view()),
]
