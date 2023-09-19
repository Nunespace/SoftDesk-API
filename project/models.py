from django.db import models

from django.conf import settings



class Project(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name="projets", null=True
    )
    name = models.CharField(max_length=500, verbose_name="Nom du projet")
    description = models.TextField(
        max_length=3000, blank=True, verbose_name="Description"
    )

    class Type(models.TextChoices):
        BACK_END = "Back-end"
        FRONT_END = "Front-end"
        ANDROID = "Androïd"

    type = models.CharField(choices=Type.choices, max_length=10)
    # contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projets", verbose_name="Contributeurs")

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

   
        

"""
    def author_is_contributor(self):
        self.contributors.add(self.request.user.id)
        print("self.contributors", self.request.user.id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.author_is_contributor()
"""


class Issue(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name="issue_author", null=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    name = models.CharField(max_length=500, verbose_name="Nom du problème")
    description = models.TextField(
        max_length=3000, blank=True, verbose_name="Description"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Attribué à ",
        related_name="issue_assigned_to",
        null=True,
    )

    STATUS = [
        ("TO_DO", "A_faire"),
        ("IN_PROGRESS", "En_cours"),
        ("FINISHED", "Terminé"),
    ]

    status = models.CharField(choices=STATUS, max_length=15, default="TO_DO")

    class Priority(models.TextChoices):
        LOW = "Basse"
        MEDIUM = "Moyenne"
        HIGH = "Haute"

    priority = models.CharField(choices=Priority.choices, max_length=15)

    class Tag(models.TextChoices):
        BUG = "Bug"
        FEATURE = "Fonctionnalité"
        TASK = "Tâche"

    tag = models.CharField(choices=Tag.choices, max_length=15)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["project"]

    def __str__(self):
        return self.name



class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name="comment_author",
    )
    # uuid : [PK]
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="Comments",
    )
    description = models.TextField(
        max_length=3000, blank=True, verbose_name="Description"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["issue"]

    def __str__(self):
        return self.issue


class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_contributor"
    )
    project = models.ForeignKey(
        'project.Project', on_delete=models.CASCADE, related_name="contributors"
    )

    class Meta:
        unique_together = ("user", "project")
