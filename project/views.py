from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from project.permissions import IsAuthorOrReadOnly, IsContributorOrReadOnly
from .models import Project, Issue, Comment, Contributor
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    # attribut de classe qui permet de définir le serializer de détail
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == "retrieve":
            return self.detail_serializer_class
        # dans tous les autres cas, retourne serializer par défaut
        return super().get_serializer_class()

    def get_queryset(self):
        """ Récupère tous les projets d'un auteur avec l'URL : http://127.0.0.1:8000/api/projects/?author_id=<author_id>"""
        # Récupère tous les projets dans une variable nommée queryset
        queryset = Project.objects.all()
        # Vérifie la présence du paramètre ‘author_id’ dans l’url et si oui alors appliquons notre filtre
        author_id = self.request.GET.get("author_id")
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    def perform_create(self, serializer):
        """L'utilisateur qui crée le projet en est l'auteur"""
        serializer.save(author=self.request.user)
     

class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorOrReadOnly]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

"""
    def perform_create(self, serializer):
        L'utilisateur qui crée le problème (issue) en est l'auteur
        serializer.save(author=self.request.user) 

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])
    """


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_create(self, serializer):
        """L'utilisateur qui crée un commentaire en est l'auteur"""
        serializer.save(author=self.request.user)


class ContributorViewSet(ModelViewSet, ReadOnlyModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        # Nous récupérons tous les contributeurs dans une variable nommée queryset
        queryset = Contributor.objects.all()
        # Vérifions la présence du paramètre ‘project_id’ dans l’url et si oui alors appliquons notre filtre
        project_id = self.request.GET.get("project_id")
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
