from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from project.models import Project


class IsSuperUserOrReadOnly(BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        # Seul le super utilisateur peut créer un utilisateur
        if request.user.is_superuser:
            print("isSuperUser")
            return True

        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            print("if Safemethod")
            return True
        
        if request.method in self.edit_methods and request.user.is_authenticated:
            print("EditMethod")
            return True

        print("else!!")

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            print("PermAuteursuperuser")
            return True
        if request.method in permissions.SAFE_METHODS:
            ("permAuteuriSafemeth")
            return True
        # un utilisateur peut modifier ou supprimer ses données (RGPD : droit à l’accès et à la rectification et droit à l'oubli)
        if obj == request.user and request.method in self.edit_methods:
            print("permAuteurObjAuthor", obj, "request.user: ", request.user)
            return True
        print("???")
        return False