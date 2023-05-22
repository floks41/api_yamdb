from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Доступ разрешен только администратору,
    проверка на уровне представления.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """Небезопасные методы HTTP разрешены только администратору.
    Проверка на уровне представления.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAuthorModeratorAdminOrReadonly(BasePermission):
    """Небезопасные методы HTTP разрешены только
    автору, модератору или администратору.
    В остальные случаях разрешены безопасные методы HTTP: GET, HEAD, OPTIONS.
    POST метод разрешен только авторизованным пользователям.
    """
    def has_object_permission(self, request, view, obj):
        """Ограничение на уровне объекта."""
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (obj.author == request.user
                 or request.user.is_project_staff))
