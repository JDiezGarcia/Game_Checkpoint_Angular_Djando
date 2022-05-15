
from rest_framework import permissions

class IsAdminUsr(permissions.BasePermission):
    message = 'You don\'t have admin permissions'

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated
                and request.user.role == 'ADMIN')


class IsSuperAdminUsr(permissions.BasePermission):
    message = 'You don\'t have admin permissions'

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated
                and request.user.is_superuser)
