# Generated by Django 4.2 on 2024-08-12 04:49

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('tour_form', '0009_touroffer_answered_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touroffer',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=85, scale=None, size=[1920, 1080], upload_to='tour_offers', verbose_name='Изображение'),
        ),
    ]
