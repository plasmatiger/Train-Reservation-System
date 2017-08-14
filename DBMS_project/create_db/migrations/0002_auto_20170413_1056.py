# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatAvailabilty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('threeA_avail', models.IntegerField()),
                ('threeA_wait', models.IntegerField()),
                ('twoA_avail', models.IntegerField()),
                ('twoA_wait', models.IntegerField()),
                ('oneA_avail', models.IntegerField()),
                ('oneA_wait', models.IntegerField()),
                ('sleeper_avail', models.IntegerField()),
                ('sleeper_wait', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PNR', models.CharField(unique=True, max_length=10)),
                ('BookedDate', models.DateField()),
                ('DateofJourney', models.DateField()),
                ('Status', models.CharField(max_length=10)),
                ('Cost', models.IntegerField()),
                ('No_of_passanges', models.IntegerField()),
                ('pass1', models.CharField(max_length=20)),
                ('pass2', models.CharField(max_length=20)),
                ('pass3', models.CharField(max_length=20)),
                ('pass4', models.CharField(max_length=20)),
                ('pass5', models.CharField(max_length=20)),
                ('pass6', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='station',
            name='StationCode',
            field=models.CharField(unique=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='train',
            name='Destination',
            field=models.ForeignKey(related_name='destination', to='create_db.Station'),
        ),
        migrations.AlterField(
            model_name='train',
            name='TrainNumber',
            field=models.IntegerField(unique=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='From',
            field=models.ForeignKey(related_name='fromm', to='create_db.Station'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='TrainName',
            field=models.ForeignKey(to='create_db.Train'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='to',
            field=models.ForeignKey(related_name='to', to='create_db.Station'),
        ),
        migrations.AddField(
            model_name='seatavailabilty',
            name='TrainNumber',
            field=models.ForeignKey(to='create_db.Train'),
        ),
    ]
