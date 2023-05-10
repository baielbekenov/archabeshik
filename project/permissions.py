from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользователи с правами администратора могут изменять и удалять объекты,
    в то время как другие пользователи могут только просматривать объекты.
    """
    def has_permission(self, request, view):
        # Возвращаем True для безопасных методов (GET, HEAD, OPTIONS).
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь администратором.
        return request.user and request.user.is_staff
