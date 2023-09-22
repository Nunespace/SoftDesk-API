from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from project.models import Project


class IsAdminAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)



class IsAuthorOrReadOnly(BasePermission):
    """
    Autorisation personnalisée d’autoriser uniquement les auteurs d’un objet à l’éditer.
    """

    def has_object_permission(self, request, view, obj):
        # Les autorisations de lecture sont autorisées à toute demande,
        # Nous autoriserons donc toujours les demandes GET, HEAD ou OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Les autorisations d’écriture ne sont autorisées qu’à l'auteur (author).
        return obj.author == request.user


class IsContributorOrReadOnly(BasePermission):
    """
    Autorisation personnalisée d’autoriser uniquement les contributeurs d’un projet à éditer un problème(issue).
    """

    def has_object_permission(self, request, view, obj):
        return bool(obj.project.contributors.filter(user=request.user).exists())

"""
    def has_permission(self, request, view):
        #id = view.kwargs['pk']
        #id = request.POST['project_id']
        obj = get_object_or_404(Project, pk=pk)
        return bool(obj.project.contributors.filter(user=request.user).exists())
"""

class ProjectIsAuthenticatedOrAuthorOrReadOnly(BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE")
"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
"""

    def has_object_permission(self, request, view, obj):

        #if request.method == "POST"

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user and request.method in self.edit_methods:
            return True

        return False
    