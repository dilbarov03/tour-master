# Generated by Django 4.0.6 on 2024-08-08 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tour_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('tg_username', models.CharField(max_length=255, verbose_name='Username в Telegram')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Общая стоимость')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tour_catalog.tour', verbose_name='Тур')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
        migrations.CreateModel(
            name='UserBookingPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.PositiveIntegerField(verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая стоимость')),
                ('tour_price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bookings', to='tour_catalog.tourprice', verbose_name='Цена на тур')),
                ('user_booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_prices', to='tour_catalog.userbooking', verbose_name='Бронирование')),
            ],
            options={
                'verbose_name': 'Цена на тур в бронировании',
                'verbose_name_plural': 'Цены на тур в бронировании',
            },
        ),
    ]
