# Generated by Django 4.0.6 on 2024-08-07 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tour_form', '0002_alter_city_country_alter_country_tour_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_date', models.DateField(verbose_name='Дата начала')),
                ('to_date', models.DateField(verbose_name='Дата окончания')),
                ('holidays', models.PositiveIntegerField(verbose_name='Количество дней отдыха')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефон')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('answered_at', models.DateTimeField(blank=True, null=True, verbose_name='Ответили')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_forms', to='tour_form.city', verbose_name='Город')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_forms', to='tour_form.country', verbose_name='Страна')),
                ('tour_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_forms', to='tour_form.tourtype', verbose_name='Тип тура')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_forms', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка на тур',
                'verbose_name_plural': 'Заявки на туры',
            },
        ),
        migrations.CreateModel(
            name='TourPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('gender', models.CharField(max_length=15, verbose_name='Пол')),
                ('tour_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_people', to='tour_form.tourform', verbose_name='Заявка на тур')),
            ],
            options={
                'verbose_name': 'Человек в заявке',
                'verbose_name_plural': 'Люди в заявке',
            },
        ),
        migrations.CreateModel(
            name='TourOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='tour_offers', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Текст')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='Статус')),
                ('tour_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_offers', to='tour_form.tourform', verbose_name='Заявка на тур')),
            ],
            options={
                'verbose_name': 'Предложение по туру',
                'verbose_name_plural': 'Предложения по турам',
                'ordering': ['-created_at'],
            },
        ),
    ]
