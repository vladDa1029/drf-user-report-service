from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    role_display = serializers.CharField(
        source="get_role_display",
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "status",
            "status_display",
            "role",
            "role_display",
            "registered_at",
            "created_at",
            "updated_at",
        ]
