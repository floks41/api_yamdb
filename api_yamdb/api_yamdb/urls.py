from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import AuthGetTokenView, AuthSignUpView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls', namespace='api')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
urlpatterns += [
     path('api/v1/auth/token/', AuthGetTokenView.as_view()),
     path('api/v1/auth/signup/', AuthSignUpView.as_view()),
]