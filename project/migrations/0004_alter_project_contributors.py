# Generated by Django 4.2.5 on 2023-09-22 16:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0003_alter_project_contributors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="contributors",
            field=models.ManyToManyField(
                db_table="Contributor",
                null=True,
                related_name="contributors",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
