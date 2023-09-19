from user.models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet


class UserViewset(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
