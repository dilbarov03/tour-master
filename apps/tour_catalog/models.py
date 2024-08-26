from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models import Min, Sum
from django_resized import ResizedImageField

from apps.common.models import BaseModel
from apps.tour_catalog.managers import TourManager, TourPriceManager


class TourCategory(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Kategoriya nomi')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    order = models.PositiveIntegerField(default=1, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Turpaket kategoriya'
        verbose_name_plural = 'Turpaket kategoriyalari'
        ordering = ['order']

    def __str__(self):
        return self.name


class Tour(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Tur nomi')
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE, verbose_name='Kategoriya',
                                 related_name='tours')
    description = RichTextUploadingField(verbose_name='Tavsif')
    image = ResizedImageField(upload_to='tour_images', verbose_name='Rasm')
    start_date = models.DateField(verbose_name='Boshlanish sanasi')
    days_count = models.PositiveIntegerField(verbose_name='Kunlar soni')
    people_count = models.PositiveIntegerField(verbose_name='Odamlar soni')
    barcode = models.CharField(max_length=255, verbose_name='Shtrixkod', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        verbose_name = 'Tur paket'
        verbose_name_plural = 'Tur paketlar'

    def __str__(self):
        return self.name


class TourPrice(BaseModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Tur', related_name='prices')
    name = models.CharField(max_length=255, verbose_name='Nomi')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Narx')
    people_count = models.PositiveIntegerField(verbose_name='Odamlar soni')
    order = models.PositiveIntegerField(default=1, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Tur uchun narx'
        verbose_name_plural = 'Tur uchun narxlar'
        ordering = ['order']

    def __str__(self):
        return f'{self.tour.name} - {self.name} - {self.price}'


class UserBooking(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Sotuvchi',
                             related_name='bookings')
    region = models.ForeignKey('users.Region', on_delete=models.SET_NULL, verbose_name='Hudud',
                                 related_name='bookings', null=True, blank=True)
    branch = models.ForeignKey('users.Branch', on_delete=models.SET_NULL, verbose_name='Filial',
                                 related_name='bookings', null=True, blank=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Tur', related_name='bookings')
    full_name = models.CharField(max_length=255, verbose_name='Mijoz')
    tg_username = models.CharField(max_length=255, verbose_name='Telegramdagi username')
    phone = models.CharField(max_length=20, verbose_name='Telefon', null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Sotuv narxi',
                                      null=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Kirim narxi',
                                         null=True, blank=True)
    region = models.ForeignKey('users.Region', on_delete=models.SET_NULL, verbose_name='Hudud',
                               related_name='bookings', null=True, blank=True)
    is_bought = models.BooleanField(default=False, verbose_name='Sotildi')

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

    def __str__(self):
        return f'{self.full_name} - {self.tour.name}'

    @property
    def total_price_formatted(self):
        return f"{self.total_price:,.0f}".replace(",", " ")

    @property
    def original_price_formatted(self):
        return f"{self.original_price:,.0f}".replace(",", " ") if self.original_price else "-"

    @property
    def people_count(self):
        return self.tour_prices.aggregate(people_count=Sum('count'))['people_count']

    total_price_formatted.fget.short_description = 'Sotuv narxi'
    original_price_formatted.fget.short_description = 'Kirim narxi'
    people_count.fget.short_description = 'Odamlar soni'


class UserBookingPrice(BaseModel):
    user_booking = models.ForeignKey(UserBooking, on_delete=models.CASCADE, verbose_name='Buyurtma',
                                     related_name='tour_prices')
    tour_price = models.ForeignKey(TourPrice, on_delete=models.CASCADE, verbose_name='Tur uchun narx',
                                   related_name='user_bookings')
    count = models.PositiveIntegerField(verbose_name='Miqdor')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Umumiy narx')

    class Meta:
        verbose_name = 'Buyurtmadagi tur narxi'
        verbose_name_plural = 'Buyurtmadagi tur narxlari'

    def __str__(self):
        return f'{self.user_booking.full_name} - {self.tour_price.tour.name} - {self.tour_price.name} - {self.count}'
