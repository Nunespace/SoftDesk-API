from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from project.models import Project, Issue
from user.models import User


class IsAuthorProject(BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        print("IsAuthorProject : has_permission executée")
        project_id = view.kwargs.get("project_pk")
        id_in_url = view.kwargs.get("pk")
        print("N° projet : ", project_id)
        print("id in url : ", id_in_url)

        if request.user.is_superuser:
            print("Permission accordée au Superutilisateur")
            return True

        # L'utilisateur connecté peut voir la liste des projets ou créer un projet et en devient l'auteur (http://127.0.0.1:8000/api/projects/)
        if project_id is None and id_in_url is None:
            if request.method == "POST" or request.method == "GET":
                print("l'utilisateur authentifié est autorisé à créer un projet ou voir la liste des projets non détaillée")
                return True

        # Seul l'auteur d'un projet peut le modifier ou le supprimer (http://127.0.0.1:8000/api/projects/<id>/)
        if project_id is None and id_in_url is not None:
            project_id = id_in_url
            project = Project.objects.get(pk=project_id)
            author = project.author
            print(
                "L'utilisateur est-il l'auteur?",
                bool(request.user and request.user == author),
            )
            return bool(request.user and request.user == author)

        print("La permission n'est pas accordée")
        return False


class IsAuthorIssue(BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        print("IsAuthorIssue : has_permission executée")
        project_id = view.kwargs.get("project_pk")
        issue_id = view.kwargs.get("issue_pk")
        id_in_url = view.kwargs.get("pk")
        print("N° projet : ", project_id)
        print("N° du problème (issue) : ", issue_id)
        print("id in url : ", id_in_url)

        if request.user.is_superuser:
            print("Permission accordée au Superutilisateur")
            return True

        # L'auteur d'un projet peut créer un problème (issue) (http://127.0.0.1:8000/api/projects/<project_id>/issues)
        # Il devient aussi auteur du problème
        if id_in_url is None:
            project = Project.objects.get(pk=project_id)
            author = project.author
            print(
                "L'utilisateur est-il l'auteur du projet?",
                bool(request.user and request.user == author),
            )
            return bool(request.user and request.user == author)

        if id_in_url is not None:
            return True

        print("La permission n'est pas accordée")
        return False

    def has_object_permission(self, request, view, obj):
        print("IsAuthorIssue : has_object_permission executée")
        print(
            f"L'auteur du problème n°{obj.id} du projet n°{view.kwargs.get('project_pk')} est {obj.author}"
        )

        if request.user.is_superuser:
            print("Permission accordée au Superutilisateur")
            return True

        # Seul l'auteur d'un problème peut le modifier ou le supprimer
        if obj.author == request.user:
            print(
                "L'utilisateur est-il l'auteur du problème?",
                bool(obj.author == request.user),
            )
            return True

        print("La permission n'est pas accordée")
        return False

class IsAuthorComment(BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        print("IsAuthorComment : has_permission executée")
        project_id = view.kwargs.get("project_pk")
        issue_id = view.kwargs.get("issue_pk")
        id_in_url = view.kwargs.get("pk")
        print("N° projet : ", project_id)
        print("N° du problème (issue) : ", issue_id)
        print("id in url : ", id_in_url)

        if request.user.is_superuser:
            print("Permission accordée au Superutilisateur")
            return True

        # L'auteur d'un projet peut créer un commentaire  (http://127.0.0.1:8000/api/projects/<project_id>/issues/<issue_id>)
        # Il devient aussi auteur du problème
        if id_in_url is None:
            project = Project.objects.get(pk=project_id)
            author = project.author
            print(
                "L'utilisateur est-il l'auteur du projet?",
                bool(request.user and request.user == author),
            )
            return bool(request.user and request.user == author)

        if id_in_url is not None:
            return True

        print("La permission n'est pas accordée")
        return False

    def has_object_permission(self, request, view, obj):
        print("IsAuthorComment : has_object_permission executée")
        print(
            f"L'auteur du commentaire n°{obj.id} du problème n°{view.kwargs.get('issue_pk')} projet n°{view.kwargs.get('project_pk')} est {obj.author}"
        )

        if request.user.is_superuser:
            print("Permission accordée au Superutilisateur")
            return True

        # Seul l'auteur d'un problème peut le modifier ou le supprimer
        if obj.author == request.user:
            print(
                "L'utilisateur est-il l'auteur du commentaire?",
                bool(obj.author == request.user),
            )
            return True

        print("La permission n'est pas accordée")
        return False

class IsContributor(BasePermission):
    edit_methods = "POST"

    def has_permission(self, request, view):
        print("IsContributor : has_permission executée")
        project_id = view.kwargs.get("project_pk")
        id_in_url = view.kwargs.get("pk")
        print("N° projet : ", project_id)
        print("id in url : ", id_in_url)

        if request.user.is_superuser:
            print("Permission accordée au Superutilisateur")
            return True

        if project_id is not None:
            project = Project.objects.get(pk=project_id)
            contributors = project.contributors.all()
            print(f"Les contributeurs du projet n°{project_id} sont : {contributors}")

            print(
                f"L'utilisateur {request.user} en fait-il parti?",
                bool(
                    request.user
                    and request.user.is_authenticated
                    and request.user in contributors
                ),
            )
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user in contributors
            )
        if project_id is None and id_in_url is not None:
            project = Project.objects.get(pk=id_in_url)
            contributors = project.contributors.all()
            print(f"Les contributeurs du projet n°{id_in_url} sont : {contributors}")
            print(
                "L'utilisateur en fait-il parti?",
                bool(
                    request.user
                    and request.user.is_authenticated
                    and request.user in contributors
                ),
            )
            return request.user in contributors

        print("La permission n'est pas accordée")
        return False

    def has_object_permission(self, request, view, obj):
        print("IsContributor : has_object_permission executée")
        print("Cible url : ", obj)

        if request.user.is_superuser:
            print("Permission accordée au Superutilisateur")
            return True

        if request.method in permissions.SAFE_METHODS:
            print("Safe method?", request.method in permissions.SAFE_METHODS)
            return True

        print("La permission n'est pas accordée")
        return False
