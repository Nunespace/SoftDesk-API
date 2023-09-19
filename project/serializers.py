from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
#from user.models import User


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        
        read_only_fields = ["author"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ["author"]

    """
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    """


class ProjectListSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
            "description",
            "type",
            "created_time",
        ]

    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Project.objects.filter(name=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Ce projet existe déjà')
        return value


class ProjectDetailSerializer(serializers.ModelSerializer):
    # contributors = serializers.StringRelatedField(many=True)
    contributors = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(), many=True)
    issues = IssueSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
            "description",
            "type",
            "contributors",
            "issues",
            "created_time",
        ]
        #read_only_fields = ["author"]

    """
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    """


class ContributorSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    # user = serializers.StringRelatedField(many=True)
    # avec get_project .......project = serializers.SerializerMethodField()

    class Meta:
        model = Contributor

        fields = ['id', 'user', 'project']
    
    """
    def get_project(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.project.objects.all()
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProjectSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
    """
    
