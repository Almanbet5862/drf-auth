from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("Необходимо задать пользователя"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Доступ к админ панели is_staff=False."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Статус суперпользователя is_superuser=False."))
        user = self.create_user(username, password, **extra_fields)
        user.save()
        return user

    def create_app_user(self, username, **extra_fields):
        if not username:
            raise ValueError(_("Необходимо задать пользователя"))
        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, **extra_fields)
        user.save()
        return user
