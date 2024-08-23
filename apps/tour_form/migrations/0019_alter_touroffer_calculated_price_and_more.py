# Generated by Django 4.2 on 2024-08-23 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_form', '0018_touroffer_calculated_price_touroffer_original_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touroffer',
            name='calculated_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='Hisoblangan narx'),
        ),
        migrations.AlterField(
            model_name='touroffer',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='Haqiqiy narx'),
        ),
    ]
