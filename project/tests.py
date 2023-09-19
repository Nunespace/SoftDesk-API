from django.test import TestCase
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from user.models import User
from project.models import Project


class TestProject(APITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy("project-list")

    def format_datetime(self, value):
        # Cette méthode est un helper permettant de formater une date en chaine de caractères sous le même format que celui de l’api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        # Création d'un projet test
        #user = User.objects.filter(id=1)
        project = Project.objects.create(
            #author=user,
            name="Projet test",
            #author=user,
            description="Ceci est un test",
            type="Back-end",
        )

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                "id": self.project.pk,
                "author": self.project.author,
                "name": self.project.name,
                "type": self.project.type,
                "description": self.project.description,
                "created_time": self.format_datetime(project.created_time),
            }
        ]
        self.assertEqual(excepted, response.json())

    """ 
    def test_create(self):
        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        self.assertFalse(Project.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouveau Projet'})
        # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertFalse(Project.objects.exists())
    """
