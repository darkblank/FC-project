# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 10:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateTimeField()),
                ('payment_date', models.DateTimeField()),
                ('price', models.PositiveIntegerField()),
                ('party', models.PositiveIntegerField()),
                ('reservation_number', models.PositiveIntegerField(unique=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('information', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurants.ReservationInfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]