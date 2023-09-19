
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

# from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from project.permissions import IsAdminAuthenticated, IsAuthorOrReadOnly
from .models import Project, Issue, Comment, Contributor
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectAdminViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


    def get_queryset(self):
        #Récupère tous les projets d'un auteur avec l'URL : http://127.0.0.1:8000/api/project/?category_id=[authors'id]
        # Récupére tous les projets dans une variable nommée queryset
        queryset = Project.objects.all()
        # Vérifie la présence du paramètre ‘author_id’ dans l’url et si oui alors appliquons notre filtre
        author_id = self.request.GET.get("author_id")
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset
    """
    def perform_create(self, serializer):
        user = serializer.validated_data.get('author')
        serializer.save(author=user)
    """
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ProjectViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        # dans tous les autres cas, retourne serializer par défaut
        return super().get_serializer_class()

    def get_queryset(self):
        # Récupére tous les projets dans une variable nommée queryset
        queryset = Project.objects.all()
        # Vérifie la présence du paramètre ‘author_id’ dans l’url et si oui alors appliquons notre filtre
        author_id = self.request.GET.get("author_id")
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()



class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewset(ModelViewSet, ReadOnlyModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        # Nous récupérons tous les contributeurs dans une variable nommée queryset
        queryset = Contributor.objects.all()
        # Vérifions la présence du paramètre ‘project_id’ dans l’url et si oui alors appliquons notre filtre
        project_id = self.request.GET.get("project_id")
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
