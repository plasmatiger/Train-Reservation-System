# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_db', '0002_auto_20170413_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Ticket', models.ForeignKey(to='create_db.Ticket')),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='Email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AddField(
            model_name='bookedticket',
            name='UserName',
            field=models.ForeignKey(to='create_db.Users'),
        ),
    ]
