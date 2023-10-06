from user.models import User
from .serializers import UserDetailSerializer, UserListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSuperUserOrReadOnly


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    list_serializer_class = UserListSerializer
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()
