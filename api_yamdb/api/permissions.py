from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class OnlyAdminPermission(permissions.BasePermission):
    """Доступ разрешен только администраторам."""

    message = 'Доступ к данной операции разрешен только администраторам.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.role == 'admin' or
                request.user.is_superuser or
                view.kwargs.get('username') == 'me'
        )

    def has_object_permission(self, request, view, obj):
        if view.kwargs.get('username') == 'me':
            return request.user == obj
        return True


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Редактирование объекта доступно только для Администратора.
    Для чтения доступно всем.
    """
    message = 'Доступно только для Администратора'

    # def has_permission(self, request, view):
    #     return request.method in permissions.SAFE_METHODS or (
    #             request.user.is_authenticated and request.user.is_admin)
    #
    # def has_object_permission(self, request, view, obj):
    #     return request.method in permissions.SAFE_METHODS or (
    #             request.user.is_authenticated and request.user.is_admin)

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # else:
        #     return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin)

      
class ReadOnlyOrAuthorOrAdmin(permissions.BasePermission):
    """Доступ на чтение для всех. Изменение - только авторам/админам."""

    message = 'У вас недостаточно прав для выполнения данной операции.'

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if (
                request.user.is_authenticated
                and
                (
                        request.user.role in ('admin', 'moderator')
                        or
                        request.user.is_superuser)
                ):
            return True
        return request.user.is_authenticated and request.user == obj.author