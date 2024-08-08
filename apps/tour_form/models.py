from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

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


class TourForm(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Пользователь",
                             related_name="tour_forms")
    region = models.ForeignKey("users.Region", on_delete=models.CASCADE, verbose_name="Регион",
                               related_name="tour_forms", null=True)
    tour_type = models.ForeignKey(TourType, on_delete=models.CASCADE, verbose_name="Тип тура",
                                  related_name="tour_forms")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна",
                                related_name="tour_forms")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город",
                             related_name="tour_forms")
    room_count = models.PositiveIntegerField(verbose_name="Количество комнат", default=0)
    from_date = models.DateField(verbose_name="Дата начала")
    to_date = models.DateField(verbose_name="Дата окончания")
    holidays = models.PositiveIntegerField(verbose_name="Количество дней отдыха")
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    comment = models.TextField(verbose_name="Комментарий")
    answered_at = models.DateTimeField(null=True, blank=True, verbose_name="Ответили")

    class Meta:
        verbose_name = "Заявка на тур"
        verbose_name_plural = "Заявки на туры"

    def __str__(self):
        return f"{self.user} - {self.country.name} - {self.city.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.region = self.user.region
        super().save(force_insert, force_update, using, update_fields)


class TourPeople(BaseModel):
    tour_form = models.ForeignKey(TourForm, on_delete=models.CASCADE, verbose_name="Заявка на тур",
                                  related_name="tour_people")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=15, verbose_name="Пол")

    class Meta:
        verbose_name = "Человек в заявке"
        verbose_name_plural = "Люди в заявке"

    def __str__(self):
        return self.full_name


class TourOffer(BaseModel):
    class Status(models.TextChoices):
        NEW = "new"
        THINKING = "thinking"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    tour_form = models.OneToOneField(TourForm, on_delete=models.CASCADE, verbose_name="Заявка на тур",
                                  related_name="tour_offer")
    image = ResizedImageField(upload_to="tour_offers", verbose_name="Изображение")
    text = RichTextUploadingField(verbose_name="Текст")
    status = models.CharField(max_length=255, verbose_name="Статус", choices=Status.choices, default=Status.NEW)

    class Meta:
        verbose_name = "Предложение по туру"
        verbose_name_plural = "Предложения по турам"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:50]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.tour_form.answered_at = timezone.now()
            self.tour_form.save()
        super().save(force_insert, force_update, using, update_fields)
