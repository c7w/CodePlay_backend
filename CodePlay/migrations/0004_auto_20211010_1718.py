# Generated by Django 3.1.5 on 2021-10-10 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodePlay', '0003_auto_20211010_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sketch',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('colors', models.IntegerField()),
                ('data', models.TextField()),
                ('hidden', models.BooleanField(default=False)),
                ('defaultValue', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='scheme',
            name='submission_time',
            field=models.BigIntegerField(default=1633857524.909145),
        ),
        migrations.AlterField(
            model_name='sessionpool',
            name='expireAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 17, 18, 44, 899150)),
        ),
    ]