from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from project.models import Project


class User(AbstractUser):
    """
    USER = 'USER'
    CONTRIBUTOR = 'CONTRIBUTOR'
    ROLE_CHOICES = (
        (USER, "Utilisateur"),
        (CONTRIBUTOR, "Contributeur"),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    """
    age = models.PositiveIntegerField(validators=[MinValueValidator(15)], default=44)
    can_be_contacted = models.BooleanField(default=False)
    can_be_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.username

"""
Vu ds le quizz 2
@action(detail=False, methods=['post'])

    def invite(self, request):

        self.send_invitation_email(self.request.POST.get('email'))

        return Response()
L’action doit être sur la liste puisque l’utilisateur à inviter ne dispose pas de compte et que l’URL le précise (aucun identifiant n’est présent). La méthode à utiliser est POST, et doit être une liste même lorsqu'une seule méthode est utilisée pour l’action.
"""