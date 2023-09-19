from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminAuthenticated(BasePermission):
    """
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
    
    def has_permission(self, request, view):
        projet = request.META['REMOTE_ADDR']
        user = request.user
        projets_of_user = User.objects.all().user
        User.objects.filter(projets=ip_addr).exists()
        return not blocked
    """

    def has_permission(self, request, view):
        obj = get_object_or_404()
        return bool(request.user and request.user.is_authenticated and obj.author == request.user)


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user
    