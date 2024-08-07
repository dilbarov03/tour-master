# Generated by Django 4.0.6 on 2024-08-07 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_form', '0004_tourform_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourform',
            name='room_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество комнат'),
        ),
        migrations.AlterField(
            model_name='touroffer',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('thinking', 'Thinking'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='new', max_length=255, verbose_name='Статус'),
        ),
    ]
