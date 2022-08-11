from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True       
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin
        return False
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin
        return False

class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if (not request.user.is_authenticated):
            return True
        return (obj.author == request.user)