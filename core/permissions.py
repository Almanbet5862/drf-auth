from rest_framework import permissions


def is_admin_user(user):
    return user.is_admin


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return is_admin_user(request.user)
