from user.models import User
from .serializers import UserDetailSerializer, UserListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    list_serializer_class = UserListSerializer

    def get_serializer_class(self):
        # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == "list":
            return self.list_serializer_class
        # dans tous les autres cas, retourne serializer par défaut
        return super().get_serializer_class()

"""
    def get_queryset(self):
        return User.objects.all()
"""
