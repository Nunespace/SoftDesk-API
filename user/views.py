from user.models import User
from .serializers import UserDetailSerializer, UserListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSuperUserOrReadOnly


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]

    def get_serializer_class(self):
        # Si l'action demandée est retrieve nous retournons le serializer de détail
        if (
            self.action == "retrieve"
            or self.action == "update"
            or self.action == "partial_update"
            or self.action == "destroy"
        ):
            return self.detail_serializer_class
        # dans tous les autres cas, retourne serializer par défaut
        return super().get_serializer_class()


