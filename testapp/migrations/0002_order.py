# Generated by Django 5.0 on 2023-12-13 14:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.FloatField(verbose_name='Сумма')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='testapp.restaurant', verbose_name='Ресторан')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
