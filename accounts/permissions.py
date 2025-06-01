from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Allows access only to users with the admin role."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManager(BasePermission):
    """Allows access only to users with the manager role."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']

class IsUser(BasePermission):
    """Allows access to all authenticated users (including user role)."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
