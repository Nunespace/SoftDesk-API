from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):

    #  l’âge légal pour donner son consentement seul est de 15 ans
    age = models.PositiveIntegerField(validators=[MinValueValidator(15)])
    # l’utilisateur peut donner ou non son consentement pour être contacté ou partager ses données personnelles.
    can_be_contacted = models.BooleanField(default=False)
    can_be_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.username
