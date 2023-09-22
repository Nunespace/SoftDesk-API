from user.models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

"""
    def get_queryset(self):
        return User.objects.all()
"""
