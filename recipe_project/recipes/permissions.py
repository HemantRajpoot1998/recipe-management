from rest_framework import permissions

class IsCreator(permissions.BasePermission):
    """
    Allows access only to users with role='creator'.
    """
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'profile') and request.user.profile.role == 'creator')


class IsViewer(permissions.BasePermission):
    """
    Allows access only to users with role='viewer'.
    """
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'profile') and request.user.profile.role == 'viewer')
