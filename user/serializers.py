from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from user.models import User
from project import serializers
from project.models import Project
from project.serializers import ProjectListSerializer


class UserSerializer(ModelSerializer):
    projets = ProjectListSerializer(read_only=True, many=True)
    #projets = PrimaryKeyRelatedField(read_only=True, many=True, queryset=Project.objects.all())

    
    # à essayer : projets = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'age', 'can_be_contacted', 'can_be_shared', 'projets']