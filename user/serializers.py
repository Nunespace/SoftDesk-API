from rest_framework.serializers import ModelSerializer
from user.models import User
from project.serializers import ProjectListSerializer


class UserSerializer(ModelSerializer):
    projets = ProjectListSerializer(read_only=True, many=True)
    # à essayer : projets = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'can_be_contacted', 'can_be_shared', 'projets']