# Generated by Django 4.2 on 2024-08-26 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_form', '0020_alter_touroffer_barcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourform',
            name='is_bought',
            field=models.BooleanField(default=False, verbose_name='Sotildi'),
        ),
    ]