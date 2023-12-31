from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsAuthorProject, IsContributor, IsAuthorIssue, IsAuthorComment
from .models import Project, Issue, Comment
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectDetailSerializer
    list_serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated & (IsAuthorProject | IsContributor)]

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        """L'utilisateur qui crée le projet en est l'auteur"""
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Récupère tous les projets d'un auteur avec l'URL : http://127.0.0.1:8000/api/projects/?author_id=:author_id
        Return : queryset
        """
        queryset = Project.objects.all()
        # Vérifie la présence du paramètre ‘author_id’ dans l’url
        author_id = self.request.GET.get("author_id")
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
            print(
                "ProjectViewSet : get_queryset exécutée : présence de author_id dans l'URL? True"
            )
        print(
            "ProjectViewSet : get_queryset exécutée : présence de author_id dans l'URL? False"
        )
        return queryset


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated & (IsAuthorIssue | IsContributor)]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["project_pk"])


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & (IsAuthorComment | IsContributor)]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])
