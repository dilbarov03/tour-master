# Generated by Django 4.2 on 2024-08-23 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_catalog', '0014_alter_tourprice_options_tourprice_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbooking',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Asl narx'),
        ),
    ]
