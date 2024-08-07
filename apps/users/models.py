from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel
from apps.users.managers import CustomUserManager


class Branch(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название филиала')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class Region(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название региона')

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class User(AbstractUser, BaseModel):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name or self.email
