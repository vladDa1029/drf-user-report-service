from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    permission_classes: list[type[IsAdminUser]] = [permissions.IsAdminUser]
