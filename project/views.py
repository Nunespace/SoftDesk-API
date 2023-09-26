from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsAuthorOrReadOnly, IsContributorOrReadOnly
from .models import Project, Issue, Comment
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(ModelViewSet):
    #queryset = Project.objects.all()
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

    def perform_create(self, serializer):
        """L'utilisateur qui crée le projet en est l'auteur"""
        #self.contributors.add(self.author.id)
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Récupère tous les projets d'un auteur avec l'URL : http://127.0.0.1:8000/api/projects/?author_id=<author_id>"""
        # Récupère tous les projets dans une variable nommée queryset
        queryset = Project.objects.all()
        # Vérifie la présence du paramètre ‘author_id’ dans l’url et si oui alors appliquons notre filtre
        author_id = self.request.GET.get("author_id")
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        print("c ici?")
        return queryset



class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated & (IsAuthorOrReadOnly | IsContributorOrReadOnly)]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["project_pk"])


"""
    def perform_create(self, serializer):
        L'utilisateur qui crée le problème (issue) en est l'auteur
        serializer.save(author=self.request.user) 
"""


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & (IsAuthorOrReadOnly | IsContributorOrReadOnly)]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])


"""
    def perform_create(self, serializer):
        L'utilisateur qui crée un commentaire en est l'auteur
        serializer.save(author=self.request.user)
"""
