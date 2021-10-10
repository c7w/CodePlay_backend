# Generated by Django 3.1.5 on 2021-10-09 18:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('student_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('fullname', models.TextField()),
                ('email', models.TextField()),
                ('role', models.TextField(default='User')),
            ],
        ),
        migrations.CreateModel(
            name='SessionPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionId', models.CharField(max_length=32)),
                ('expireAt', models.DateTimeField(default=datetime.datetime(2021, 10, 12, 18, 31, 54, 855153))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CodePlay.user')),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('submission_time', models.DateTimeField(default=datetime.datetime(2021, 10, 9, 18, 31, 54, 861153))),
                ('sketch_id', models.IntegerField()),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('likes', models.BigIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('colors', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CodePlay.user')),
            ],
        ),
    ]