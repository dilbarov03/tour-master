# Generated by Django 4.0.6 on 2024-08-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_branch_alter_user_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Администратор'), ('client', 'Клиент')], default='client', max_length=10),
        ),
    ]