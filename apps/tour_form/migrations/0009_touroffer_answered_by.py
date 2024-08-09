# Generated by Django 4.0.6 on 2024-08-08 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tour_form', '0008_alter_touroffer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='touroffer',
            name='answered_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ответил'),
        ),
    ]
