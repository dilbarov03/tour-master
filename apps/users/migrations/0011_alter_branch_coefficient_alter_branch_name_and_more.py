# Generated by Django 4.2 on 2024-08-19 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_branch_coefficient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='coefficient',
            field=models.FloatField(default=0, verbose_name='Koefitsient'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Filial nomi'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='users.region', verbose_name='Hudud'),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Hudud nomi'),
        ),
        migrations.AlterField(
            model_name='user',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.branch', verbose_name='Filial'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='F.I.O.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, unique=True, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='user',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.region', verbose_name='Hudud'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Administrator'), ('client', 'Mijoz')], default='client', max_length=10, verbose_name='Foydalanuvchi turi'),
        ),
    ]