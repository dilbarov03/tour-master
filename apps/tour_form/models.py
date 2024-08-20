from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

from apps.common.models import BaseModel
from apps.tour_form.managers import ActiveManager


class TourType(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib")

    objects = ActiveManager()

    class Meta:
        verbose_name = "Sayohat turi"
        verbose_name_plural = "Sayohat turlari"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    tour_type = models.ForeignKey(TourType, on_delete=models.CASCADE, verbose_name="Sayohat turi",
                                  related_name="countries")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib")

    objects = ActiveManager()

    class Meta:
        verbose_name = "Davlat va shahar"
        verbose_name_plural = "Davlatlar va shaharlar"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.tour_type.name}"


class City(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Davlat",
                                related_name="cities")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib")

    class Meta:
        verbose_name = "Shahar"
        verbose_name_plural = "Shaharlar"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.country.name} - {self.country.tour_type.name}"


class TourForm(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, verbose_name="Sotuvchi",
                             related_name="tour_forms", null=True, blank=True)
    region = models.ForeignKey("users.Region", on_delete=models.SET_NULL, verbose_name="Hudud",
                               related_name="tour_forms", null=True, blank=True)
    branch = models.ForeignKey("users.Branch", on_delete=models.SET_NULL, verbose_name="Filial",
                                 related_name="tour_forms", null=True, blank=True)
    tour_type = models.ForeignKey(TourType, on_delete=models.SET_NULL, verbose_name="Sayohat turi",
                                  related_name="tour_forms", null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name="Davlat",
                                related_name="tour_forms", null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name="Shahar",
                             related_name="tour_forms", null=True, blank=True)
    room_count = models.PositiveIntegerField(verbose_name="Xonalar soni", default=0)
    from_date = models.DateField(verbose_name="Boshlanish sanasi")
    to_date = models.DateField(verbose_name="Tugash sanasi")
    holidays = models.PositiveIntegerField(verbose_name="Dam olish kunlari soni")
    phone = models.CharField(max_length=255, verbose_name="Telefon")
    full_name = models.CharField(max_length=255, verbose_name="Mijoz", null=True, blank=True)
    comment = models.TextField(verbose_name="Izoh", null=True, blank=True)
    answered_at = models.DateTimeField(null=True, blank=True, verbose_name="Javob berilgan vaqti")
    is_bought = models.BooleanField(default=False, verbose_name="Sotib olingan")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"{self.user} - {self.country.name} - {self.city.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.region = self.user.region
        super().save(force_insert, force_update, using, update_fields)

    def has_offer(self):
        return hasattr(self, "tour_offer")

    def get_people(self):
        if hasattr(self, "tour_people"):
            return ", ".join([person.full_name for person in self.tour_people.all()])
        return "Yo'q"

    has_offer.boolean = True
    has_offer.short_description = "Taklif mavjud"


class TourPeople(BaseModel):
    tour_form = models.ForeignKey(TourForm, on_delete=models.CASCADE, verbose_name="Tur buyurtmasi",
                                  related_name="tour_people")
    full_name = models.CharField(max_length=255, verbose_name="F.I.O")
    birth_date = models.DateField(verbose_name="Tug'ilgan sanasi")
    gender = models.CharField(max_length=15, verbose_name="Jinsi")

    class Meta:
        verbose_name = "Buyurtmadagi shaxs"
        verbose_name_plural = "Buyurtmadagi shaxslar"

    def __str__(self):
        return self.full_name


class TourOffer(BaseModel):
    class Status(models.TextChoices):
        NEW = "new"
        THINKING = "thinking"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    tour_form = models.OneToOneField(TourForm, on_delete=models.CASCADE, verbose_name="Tur buyurtmasi",
                                     related_name="tour_offer")
    image = ResizedImageField(upload_to="tour_offers", verbose_name="Rasm")
    text = RichTextUploadingField(verbose_name="Matn")
    status = models.CharField(max_length=255, verbose_name="Status", choices=Status.choices, default=Status.NEW)
    barcode = models.CharField(max_length=255, verbose_name='Shtrixkod', null=True, blank=True)
    answered_by = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Javob berilgan", null=True,
                                    blank=True)

    class Meta:
        verbose_name = "Agentlik taklifi"
        verbose_name_plural = "Agentlik takliflari"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:50]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.tour_form.answered_at = timezone.now()
            self.tour_form.save()
        super().save(force_insert, force_update, using, update_fields)
