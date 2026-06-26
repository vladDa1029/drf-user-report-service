# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserStatus(models.TextChoices):
    ACTIVE = "AC", _("Active")
    INACTIVE = "IN", _("Inactive")
    BANNED = "BA", _("Banned")
    PENDING = "PE", _("Pending")
    DELETED = "DE", _("Deleted")


class UserRole(models.TextChoices):
    USER = "US", _("User")
    MANAGER = "MA", _("Manager")
    ADMIN = "AD", _("Admin")
    SUPPORT = "SU", _("Support")


class User(AbstractUser):
    status = models.CharField(
        max_length=2,
        choices=UserStatus.choices,
        default=UserStatus.PENDING,
    )
    role = models.CharField(
        max_length=2,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    registered_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} <{self.email}>"
