import uuid
from django.db import models
from django.conf import settings


class Project(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name="projets",
    )
    name = models.CharField(max_length=500, verbose_name="Nom du projet")
    description = models.TextField(
        max_length=3000, verbose_name="Description"
    )

    class Type(models.TextChoices):
        BACK_END = "back_end"
        FRONT_END = "front_end"
        ANDROID = "androïd"

    type = models.CharField(choices=Type.choices, max_length=10)
    # le modèle Project est lié au modèle User avec la table intermédiaire créée par défaut par Django et renommée "Contributor"
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="project", db_table="Contributor")

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Issue(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name="issue_author",
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues", null=True
    )
    name = models.CharField(max_length=500, verbose_name="Nom du problème")
    description = models.TextField(
        max_length=3000, verbose_name="Description"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Attribué à ",
        related_name="issue_assigned_to", null=True
    )

    STATUS = [
        ("TO_DO", "to_do"),
        ("IN_PROGRESS", "in_progress"),
        ("FINISHED", "finished"),
    ]

    status = models.CharField(choices=STATUS, max_length=15, default="A_faire")

    PRIORITY = [
        ("LOW", "low"),
        ("MEDIUM", "medium"),
        ("HIGH", "high"),
    ]

    priority = models.CharField(choices=PRIORITY, max_length=15)

    TAG = [
        ("BUG", "bug"),
        ("FEATURE", "feature"),
        ("TASK", "task"),
    ]

    tag = models.CharField(choices=TAG, max_length=15)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["project"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.assigned_to is None:
            self.assigned_to = self.author


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name="comment_author",
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    description = models.TextField(
        max_length=3000, verbose_name="Description"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["issue"]
