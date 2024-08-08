from django.db import models
from django.db.models import Min

from apps.common.models import BaseModel
from apps.tour_catalog.managers import TourManager, TourPriceManager


class TourCategory(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    order = models.PositiveIntegerField(default=1, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Категория тура'
        verbose_name_plural = 'Категории туров'
        ordering = ['order']

    def __str__(self):
        return self.name


class Tour(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название тура')
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='tours')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='tour_images', verbose_name='Изображение')
    start_date = models.DateField(verbose_name='Дата начала')
    days_count = models.PositiveIntegerField(verbose_name='Количество дней')
    people_count = models.PositiveIntegerField(verbose_name='Количество человек')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    objects = TourManager()

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def __str__(self):
        return self.name

    @property
    def min_price(self):
        min_price = self.prices.all().aggregate(Min('price'))['price__min']
        return min_price


class TourPrice(BaseModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур', related_name='prices')
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    people_count = models.PositiveIntegerField(verbose_name='Количество человек')

    objects = TourPriceManager()

    class Meta:
        verbose_name = 'Цена на тур'
        verbose_name_plural = 'Цены на туры'
        ordering = ['people_count']

    def __str__(self):
        return f'{self.tour.name} - {self.name} - {self.price}'


class UserBooking(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур', related_name='bookings')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    tg_username = models.CharField(max_length=255, verbose_name='Username в Telegram')
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость',
                                      null=True, blank=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'{self.full_name} - {self.tour.name}'


class UserBookingPrice(BaseModel):
    user_booking = models.ForeignKey(UserBooking, on_delete=models.CASCADE, verbose_name='Бронирование',
                                     related_name='tour_prices')
    tour_price = models.ForeignKey(TourPrice, on_delete=models.CASCADE, verbose_name='Цена на тур',
                                   related_name='user_bookings')
    count = models.PositiveIntegerField(verbose_name='Количество')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')

    class Meta:
        verbose_name = 'Цена на тур в бронировании'
        verbose_name_plural = 'Цены на тур в бронировании'

    def __str__(self):
        return f'{self.user_booking.full_name} - {self.tour_price.tour.name} - {self.tour_price.name} - {self.count}'

    def save(self, *args, **kwargs):
        self.total_price = self.tour_price.price * self.count
        super().save(*args, **kwargs)


