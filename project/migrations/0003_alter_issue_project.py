# Generated by Django 4.2.6 on 2023-10-06 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0002_comment_issue_alter_project_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="issues",
                to="project.project",
            ),
        ),
    ]