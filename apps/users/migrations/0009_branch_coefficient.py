# Generated by Django 4.2 on 2024-08-16 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_branch_options_alter_region_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='coefficient',
            field=models.FloatField(default=1, verbose_name='Коэффициент'),
        ),
    ]
