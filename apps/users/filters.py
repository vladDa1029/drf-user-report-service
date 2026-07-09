from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from .models import User, UserRole, UserStatus


class CustomOrderingFilter(filters.OrderingFilter):
    """Add unique/pk field towards ordering filter for make persistence ordering.

    WARN: Work for model with pk equals id
    """

    def filter(self, qs, value):
        if value is None:
            value = ["id"]
        elif "id" not in value and "-id" not in value:
            value: list[str] = value + ["id"]
        # I think it is type list (since ordering may be for several fields).
        # This impl no work for other model because everyone have field 'id'.
        return super().filter(qs, value)


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(method="filter_name")
    status = filters.ChoiceFilter(choices=UserStatus.choices)
    role = filters.ChoiceFilter(choices=UserRole.choices)
    registered_at = filters.IsoDateTimeFromToRangeFilter()
    ordering = CustomOrderingFilter(
        fields=(
            ("status", "status"),
            ("role", "role"),
            ("registered_at", "registered_at"),
        )
    )

    def filter_name(self, queryset: QuerySet[User], name: str, value: str) -> QuerySet[User]:
        if value:
            queryset = queryset.filter(
                Q(first_name__icontains=value) | Q(last_name__icontains=value)
            )
        return queryset

    class Meta:
        model = User
        fields: list[str] = []
