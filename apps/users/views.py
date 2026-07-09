from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from .filters import UserFilter
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
