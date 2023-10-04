from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    
    #  l’âge légal pour donner son consentement seul est de 15 ans
    age = models.PositiveIntegerField(validators=[MinValueValidator(15)], default=44)
    # l’utilisateur peut donner ou non son consentement pour être contacté ou partager ses données personnelles.
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