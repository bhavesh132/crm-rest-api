from rest_framework import permissions


class IsInGroup(permissions.BasePermission):
    """
    Custom permission to only allow users in a specific group to access the view.
    """

    def has_permission(self, request, view):
        # You can access the `group_name` from the view's attributes
        group_name = getattr(view, 'group_name', None)

        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if the user is in the required group
        if group_name and request.user.groups.filter(name=group_name).exists():
            return True

        return False
    
class CanViewOnlyGroups(permissions.BasePermission):
    """
    Custom permission to allow only specific group members to view (GET) the group list.
    """

    def has_permission(self, request, view):
        # Allow safe methods for the specified group
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and request.user.groups.filter(name='GroupViewers').exists()
        return False  # Disallow POST, PUT, DELETE, etc.