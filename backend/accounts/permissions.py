from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission check for admin users"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsStudentOrAdmin(permissions.BasePermission):
    """Permission check for student or admin users"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_student or request.user.is_admin
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission check for object owner or admin"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.user == request.user

