from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)
