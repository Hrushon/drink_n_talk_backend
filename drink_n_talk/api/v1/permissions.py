from rest_framework import permissions


class IsInitiatorOrAdminOnlyPermission(permissions.BasePermission):
    """Ограничивает доступ к удалению барной стойки."""

    def has_object_permission(self, request, view, obj):
        return (obj.initiator == request.user or request.user.is_superuser)
