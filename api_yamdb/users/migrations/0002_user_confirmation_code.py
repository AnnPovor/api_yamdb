# Generated by Django 2.2.16 on 2022-08-11 08:42

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=uuid.uuid4, max_length=256),
        ),
    ]
