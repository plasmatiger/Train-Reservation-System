# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('StationCode', models.CharField(max_length=5)),
                ('StationName', models.CharField(max_length=25)),
                ('City', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Type', models.CharField(max_length=2)),
                ('TrainName', models.CharField(max_length=20)),
                ('TrainNumber', models.CharField(max_length=5)),
                ('Destination', models.ForeignKey(related_name='desti', to='create_db.Station')),
                ('Source', models.ForeignKey(related_name='source', to='create_db.Station')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('FullName', models.CharField(max_length=50)),
                ('BirthDate', models.DateField()),
                ('Email', models.EmailField(unique=True, max_length=70)),
                ('Gender', models.CharField(max_length=1)),
                ('UserName', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
