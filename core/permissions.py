from rest_framework.permissions import (
    BasePermission, IsAuthenticated
)
from core.models import Users
from rest_framework.request import Request


# is active user
class IsActive(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            request.user.status == Users.Status.ACTIVE
        )


# Is amdin
class IsAdmin(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            request.user.role == Users.Roles.ADMIN
        )


# is user
class IsUser(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            IsAuthenticated.has_permission(self, request, view) and
            request.user.role == Users.Roles.USER
        )


# is not authenticated
class IsAnonymous(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            not IsAuthenticated.has_permission(self, request, view)
        )
