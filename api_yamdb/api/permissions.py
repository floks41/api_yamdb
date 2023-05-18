"""Модуль разрешений для приложения API проекта API_Yamdb."""


from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import ADMIN_ROLE, STAFF_USER_ROLES


class IsAuthorOrReadOnly(BasePermission):
    """Небезопасные методы HTTP разрешены только автору.
    В остальные случаях разрешены безопасные методы HTTP: GET, HEAD, OPTIONS.
    """
    def has_object_permission(self, request, view, obj):
        """Ограничение на уровне объекта."""
        return (
            request.user.is_superuser
            or request.method in SAFE_METHODS 
            or obj.author == request.user)


class IsAdmin(BasePermission):
    """Доступ разрешен только администратору,
    проверка на уровне представления."""
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or (request.user.is_authenticated
                and request.user.role == ADMIN_ROLE))


class IsAdminOrReadOnly(BasePermission):
    """Небезопасные методы HTTP разрешены только администратору,
    проверка на уровне представления."""
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == ADMIN_ROLE))


class IsAuthorModeratorAdminOrReadonly(BasePermission):
    """Небезопасные методы HTTP разрешены только
    автору, модератору или администратору.
    В остальные случаях разрешены безопасные методы HTTP: GET, HEAD, OPTIONS.
    POST метод разрешен только авторизованным пользователям.
    """
    def has_object_permission(self, request, view, obj):
        """Ограничение на уровне объекта."""
        return (
            request.user.is_superuser
            or request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.role in STAFF_USER_ROLES)))
