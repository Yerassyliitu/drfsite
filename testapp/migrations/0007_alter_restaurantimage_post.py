# Generated by Django 5.0 on 2023-12-14 06:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0006_rename_images_restaurantimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantimage',
            name='post',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='testapp.restaurant'),
        ),
    ]
