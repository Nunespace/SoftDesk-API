from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from project.models import Project


class User(AbstractUser):
    USER = 'USER'
    CONTRIBUTOR = 'CONTRIBUTOR'
    ROLE_CHOICES = (
        (USER, "Utilisateur"),
        (CONTRIBUTOR, "Contributeur"),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    age = models.PositiveIntegerField(validators=[MinValueValidator(15)], default=44)
    can_be_contacted = models.BooleanField(default=False)
    can_be_shared = models.BooleanField(default=False)

