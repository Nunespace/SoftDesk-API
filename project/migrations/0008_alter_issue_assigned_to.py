# Generated by Django 4.2.5 on 2023-09-27 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0007_alter_issue_assigned_to"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="assigned_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="issue_assigned_to",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Attribué à ",
            ),
        ),
    ]
