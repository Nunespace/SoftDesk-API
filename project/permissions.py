from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from project.models import Project
from user.models import User


class IsAuthorOrReadOnly(BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        # un utilisateur connecté peut créer un projet(la permission IsAuthenticated est prévue dans ProjectViewSet)
        if request.method == "POST":
            return True

        if request.method in self.edit_methods or request.method in self.permissions.SAFE_METHODS:
            if view.kwargs.get("pk") is not None:
                project_id = view.kwargs.get("pk")
                project = Project.objects.get(pk=project_id)
                author = project.author
                print("auteure : ", author, "projet n° ", project_id)

        def has_object_permission(self, request, view, obj):
            project_id = view.kwargs.get("project_pk")
            project = Project.objects.get(pk=project_id)
            author = project.author
            print("auteur : ", author, "projet n° ", project_id)
            if request.user.is_superuser:
                print("PermAuteursuperuser")
                return True
            if request.method in permissions.SAFE_METHODS or request.method == "post":
                ("permAuteuriSafemeth")
                return bool(request.user and request.user == author)
            if obj.author == request.user and request.method in self.edit_methods:
                ("permAuteurObjAuthor")
                return True
            print("???")
            return False


"""return bool(
                    request.user
                    and request.user.is_authenticated
                    and request.user == author
                )"""
# else:
# return True


class IsContributorOrReadOnly(BasePermission):
    edit_methods = "POST"

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)
        contributors = project.contributors.all()
        # contribut = User.objects.get(projetts__pk=id).contributors.all()
        print("contributeurs : ", contributors, "projet n° ", id)
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user in contributors
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            print("PermContribsuperuser")
            return True

        if request.method in permissions.SAFE_METHODS:
            print("permContriSafemeth")
            return True

        return False
