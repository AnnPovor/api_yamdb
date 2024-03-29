# Generated by Django 2.2.16 on 2022-08-17 06:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220815_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(10, message='Оценка не должна быть выше 10'), django.core.validators.MinValueValidator(1, message='Оценка не должна быть меньше 1')], verbose_name='Оценка'),
        ),
    ]
