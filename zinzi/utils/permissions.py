from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method not in permissions.SAFE_METHODS:
            return False


class IsAuthorAndStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser or request.user.is_staff:
            return True
        return obj.author == request.user


class IsOwnerOrNotAllow(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUserOrNotAllow(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class NotAllowForSpecificData(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.data.get('price') and not request.data.get('party')
