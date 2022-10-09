from rest_framework.permissions import BasePermission


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'worker'


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'client'
