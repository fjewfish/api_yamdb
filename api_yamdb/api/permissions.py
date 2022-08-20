from django.contrib.auth import get_user_model

from rest_framework import permissions

User = get_user_model()


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    allowed_user_roles = (User.ADMIN, User.MODERATOR)

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.role in self.allowed_user_roles
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Позволяет получить доступ на зпись администраторам или superuser."""
    allowed_user_roles = (User.ADMIN,)

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.role in self.allowed_user_roles:
            return True

        return False


class IsUserRole(permissions.BasePermission):
    """Позволяет получить доступ только аутентифицированным пользователям."""
    allowed_user_roles = (User.USER,)

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in self.allowed_user_roles)


class IsModeratorRole(permissions.BasePermission):
    """Позволяет получить доступ только модераторам."""
    allowed_user_roles = (User.MODERATOR,)

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in self.allowed_user_roles)


class IsAdminRole(permissions.BasePermission):
    """Позволяет получить доступ только администраторам или superuser."""
    allowed_user_roles = (User.ADMIN,)

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return (request.user.is_authenticated
                and request.user.role in self.allowed_user_roles)
