# Generated by Django 4.2.6 on 2023-10-06 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "description",
                    models.TextField(max_length=3000, verbose_name="Description"),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_author",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Auteur",
                    ),
                ),
            ],
            options={
                "ordering": ["issue"],
            },
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=500, verbose_name="Nom du problème"),
                ),
                (
                    "description",
                    models.TextField(max_length=3000, verbose_name="Description"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("TO_DO", "to_do"),
                            ("IN_PROGRESS", "in_progress"),
                            ("FINISHED", "finished"),
                        ],
                        default="A_faire",
                        max_length=15,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("LOW", "low"),
                            ("MEDIUM", "medium"),
                            ("HIGH", "high"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "tag",
                    models.CharField(
                        choices=[
                            ("BUG", "bug"),
                            ("FEATURE", "feature"),
                            ("TASK", "task"),
                        ],
                        max_length=15,
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="issue_assigned_to",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Attribué à ",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue_author",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Auteur",
                    ),
                ),
            ],
            options={
                "ordering": ["project"],
            },
        ),
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="project",
            name="contributors",
            field=models.ManyToManyField(
                db_table="Contributor",
                related_name="project",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projets",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Auteur",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(max_length=3000, verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="project",
            name="type",
            field=models.CharField(
                choices=[
                    ("back_end", "Back End"),
                    ("front_end", "Front End"),
                    ("androïd", "Android"),
                ],
                max_length=10,
            ),
        ),
        migrations.DeleteModel(
            name="Contributor",
        ),
        migrations.AddField(
            model_name="issue",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="issues",
                to="project.project",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="issue",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="project.issue",
            ),
        ),
    ]