from rest_framework import permissions


class OnlyAdminPermission(permissions.BasePermission):
    """Доступ разрешен только администраторам."""

    message = 'Доступ к данной операции разрешен только администраторам.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.role == 'admin' or
                request.user.is_superuser or
                view.kwargs['username'] == 'me'
        )

    def has_object_permission(self, request, view, obj):
        return request.user == obj
