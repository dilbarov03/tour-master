from django.db import models

from apps.common.models import BaseModel
from apps.tour_form.managers import ActiveManager


class TourType(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок")

    objects = ActiveManager()

    class Meta:
        verbose_name = "Тип тура"
        verbose_name_plural = "Типы туров"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    tour_type = models.ForeignKey(TourType, on_delete=models.CASCADE, verbose_name="Тип тура",
                                   related_name="countries")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок")

    objects = ActiveManager()

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.tour_type.name}"


class City(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна",
                                related_name="cities")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок")

    objects = ActiveManager()

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.country.name} - {self.country.tour_type.name}"

