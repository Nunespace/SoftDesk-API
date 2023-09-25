from rest_framework.serializers import ModelSerializer, StringRelatedField
from user.models import User
from project import serializers
from project.models import Project
from project.serializers import ProjectListSerializer
from django.contrib.auth.hashers import make_password


class UserDetailSerializer(ModelSerializer):
    projets = ProjectListSerializer(read_only=True, many=True)

    # projets = PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_be_shared",
            "projets",
        ]

    def validate_password(self, value: str) -> str:
        """
        Valeur de hachage passée par l’utilisateur.
        Paramètre value : mot de passe d’un utilisateur
        Retourne : une version hachée du mot de passe
        """
        return make_password(value)
    
class UserListSerializer(ModelSerializer):
    projets = StringRelatedField(read_only=True, many=True)
  

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "projets",

        ]
