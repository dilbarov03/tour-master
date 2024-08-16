from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel
from apps.users.managers import CustomUserManager


class Region(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название региона')

    class Meta:
        verbose_name = 'Hudud'
        verbose_name_plural = 'Hududlar'

    def __str__(self):
        return self.name


class Branch(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название филиала')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион', related_name='branches',
                               null=True)
    coefficient = models.FloatField(default=0, verbose_name='Коэффициент')

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiallar'

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    class UserType(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        CLIENT = 'client', 'Клиент'

    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.CLIENT)

    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Sotuvchilar'

    def __str__(self):
        return self.full_name or self.phone

    def get_userinfo(self):
        return f"{self.id} - {self.full_name}"
