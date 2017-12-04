# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 16:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_auto_20171204_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationinfo',
            name='time',
            field=models.TimeField(choices=[(datetime.time(9, 0), '9시'), (datetime.time(10, 0), '10시'), (datetime.time(11, 0), '11시'), (datetime.time(12, 0), '12시'), (datetime.time(13, 0), '13시'), (datetime.time(14, 0), '14시'), (datetime.time(15, 0), '15시'), (datetime.time(16, 0), '16시'), (datetime.time(17, 0), '17시'), (datetime.time(18, 0), '18시'), (datetime.time(19, 0), '19시'), (datetime.time(20, 0), '20시'), (datetime.time(20, 0), '21시')], max_length=50),
        ),
    ]
