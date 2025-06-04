from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == 'ADMIN'

class IsAgricultor(BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == 'AGRICULTOR'