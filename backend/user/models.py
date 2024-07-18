from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _

from backend.models import DateMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
            
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser, DateMixin):
    username = models.CharField(_("Юзернейм"), max_length=60, unique=True)
    name = models.CharField(_("Имя"), max_length=100, default='')
    mobile_phone = models.CharField(_("Номер телефона (с 8)"), max_length=50, blank=True)
    fav_discounts = models.ManyToManyField("discounts.Discount", verbose_name=_("Избранные скидки"), blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username
