from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from project.models import Project
from user.models import User


class IsAuthorOrReadOnly(BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user and request.method in self.edit_methods:
            return True

        return False


class IsContributorOrReadOnly(BasePermission):
    edit_methods = "POST"

    def has_permission(self, request, view):
        id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=id)
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
            print("superuser")
            return True

        if request.method in permissions.SAFE_METHODS:
            print("safemethodok")
            return True

        return False
