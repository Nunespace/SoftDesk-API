from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Project, Issue, Comment, Contributor


# from user.models import User


class CommentSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'issue_pk': 'issue__pk',
        'project_pk': 'issue__project__pk',
    }

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author"]

    def save(self):
        issue_id_in_url = self.context["view"].kwargs["project_pk"]
        issue_object = get_object_or_404(Issue, pk=issue_id_in_url)
        super().save(
            author=self.context["request"].user,
            issue=issue_object,
        )


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    parent_lookup_kwargs = {
        "project_pk": "project__pk",
    }

    class Meta:
        model = Issue
        fields = ["author", "project", "name", "assigned_to", "status", "comments"]
        read_only_fields = ["author"]

    def save(self):
        project_id_in_url = self.context["view"].kwargs["project_pk"]
        project_object = get_object_or_404(Project, pk=project_id_in_url)
        super().save(
            author=self.context["request"].user,
            project=project_object,
        )


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
            "description",
            "type",
            "contributors"
        ]

    def validate_name(self, value):
        # vérifie si le projet existe déjà
        if Project.objects.filter(name=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError("Ce projet existe déjà")
        return value


class ProjectDetailSerializer(serializers.ModelSerializer):
    # contributors = serializers.StringRelatedField(many=True)
    # contributors = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(), many=True)
    issues = IssueSerializer(read_only=True, many=True)
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
            "description",
            "type",
            "contributors",
            "issues",
            "created_time",
        ]
        # read_only_fields = ["issues"]


class ContributorSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    # user = serializers.StringRelatedField(many=True)
    # avec get_project .......project = serializers.SerializerMethodField()

    class Meta:
        model = Contributor

        fields = ["id", "user", "project"]

    """
    def get_project(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.project.objects.all()
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProjectSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
    """
