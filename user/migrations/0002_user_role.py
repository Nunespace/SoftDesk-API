# Generated by Django 4.2.5 on 2023-09-14 17:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("USER", "Utilisateur"), ("CONTRIBUTOR", "Contributeur")],
                default="",
                max_length=30,
                verbose_name="Rôle",
            ),
            preserve_default=False,
        ),
    ]