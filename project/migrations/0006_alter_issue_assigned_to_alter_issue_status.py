# Generated by Django 4.2.5 on 2023-09-14 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0005_alter_comment_options_alter_issue_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="assigned_to",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="issue_assigned_to",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Attribué à ",
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="status",
            field=models.CharField(
                choices=[
                    ("TO_DO", "A_faire"),
                    ("IN_PROGRESS", "En_cours"),
                    ("FINISHED", "Terminé"),
                ],
                default="TO_DO",
                max_length=15,
            ),
        ),
    ]