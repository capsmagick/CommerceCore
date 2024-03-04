from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
        Allows access only to super admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsCustomer(BasePermission):
    """
        Allows access only to customers
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_customer and not request.user.is_suspended)
