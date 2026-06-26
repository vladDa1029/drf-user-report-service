from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import User

# Group тоже рендерится в админке — перерегистрируем её через unfold,
# иначе её страница останется в стандартной теме Django.
admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # BaseUserAdmin даёт логику пароля/add-формы, ModelAdmin — тему unfold.
    # unfold-формы нужны, чтобы поля (в т.ч. смена пароля) были стилизованы.
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "status",
        "role",
        "registered_at",
        "created_at",
    )
    list_filter = ("status", "role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("id",)
    readonly_fields = ("last_login", "date_joined", "created_at", "updated_at")

    # Берём стандартные секции UserAdmin и дописываем свои поля.
    fieldsets = tuple(BaseUserAdmin.fieldsets or ()) + (
        (_("Profile"), {"fields": ("status", "role", "registered_at")}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at")}),
    )
    # Поля на шаге "Add user" (создание пользователя с паролем).
    add_fieldsets = tuple(BaseUserAdmin.add_fieldsets or ()) + (
        (_("Profile"), {"fields": ("status", "role")}),
    )
