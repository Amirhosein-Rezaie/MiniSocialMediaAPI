from rest_framework.permissions import (
    BasePermission, IsAuthenticated, SAFE_METHODS
)
from core.models import Users
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied


# is active user
class IsActive(BasePermission):
    def has_permission(self, request: Request, view):
        if request.user.status == Users.Status.ACTIVE:
            return True
        else:
            raise PermissionDenied(
                detail=f"Your account is {request.user.status}", code=403
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


# just allow PUT, DELETE, PATCH methods for owen user
class IsSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.id == request.user.id
