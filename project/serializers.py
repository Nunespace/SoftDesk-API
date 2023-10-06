from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Project, Issue, Comment


class CommentSerializer(serializers.ModelSerializer):
    # ref. : https://pypi.org/project/drf-nested-routers/
    parent_lookup_kwargs = {
        "issue_pk": "issue__pk",
        "project_pk": "issue__project__pk",
    }

    issue = serializers.ReadOnlyField(source="issue.name")

    class Meta:
        model = Comment
        fields = ["id", "author", "issue", "description"]
        read_only_fields = ["author"]

    def save(self):
        issue_id_in_url = self.context["view"].kwargs["issue_pk"]
        issue = get_object_or_404(Issue, pk=issue_id_in_url)
        super().save(
            author=self.context["request"].user,
            issue=issue,
        )


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    parent_lookup_kwargs = {
        "project_pk": "project__pk",
    }

    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "project",
            "name",
            "priority",
            "tag",
            "assigned_to",
            "status",
            "comments",
        ]
        read_only_fields = ["author"]

    def validate_name(self, value):
        """vérifie si le problème existe déjà"""
        if Issue.objects.filter(name=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError("Ce problème existe déjà")
        return value

    def validate_assigned_to(self, value):
        project_id_in_url = self.context["view"].kwargs["project_pk"]
        project = get_object_or_404(Project, pk=project_id_in_url)
        print(value)
        if value not in project.contributors.all():
            if value != project.author:
                raise serializers.ValidationError("Cet utilisateur n'est pas un contributeur ou l'auteur de ce projet")
        return value

    def save(self):
        project_id_in_url = self.context["view"].kwargs["project_pk"]
        project_id = get_object_or_404(Project, pk=project_id_in_url)
        super().save(author=self.context["request"].user, project=project_id)


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
            "type",
        ]

    def validate_name(self, value):
        # vérifie si le projet existe déjà
        if Project.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ce projet existe déjà")
        return value


class ProjectDetailSerializer(serializers.ModelSerializer):
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
