# Generated by Django 4.0.6 on 2024-08-07 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TourType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Тип тура',
                'verbose_name_plural': 'Типы туров',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Порядок')),
                ('tour_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour_form.tourtype', verbose_name='Тип тура')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Порядок')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour_form.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['order', 'name'],
            },
        ),
    ]
