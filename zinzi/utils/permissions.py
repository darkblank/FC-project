from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
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
