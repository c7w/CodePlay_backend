# Generated by Django 3.1.5 on 2021-10-10 00:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodePlay', '0002_auto_20211010_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheme',
            name='submission_time',
            field=models.BigIntegerField(default=1633797605.164944),
        ),
        migrations.AlterField(
            model_name='sessionpool',
            name='expireAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 0, 40, 5, 155961)),
        ),
    ]
