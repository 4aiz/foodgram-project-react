from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAuthenticatedAuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.method in permissions.SAFE_METHODS)
