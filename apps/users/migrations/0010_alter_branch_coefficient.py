# Generated by Django 4.2 on 2024-08-16 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_branch_coefficient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='coefficient',
            field=models.FloatField(default=0, verbose_name='Коэффициент'),
        ),
    ]