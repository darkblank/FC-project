# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 05:57
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_google_maps.fields
import utils.custom_imagefield


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_rate', models.FloatField(choices=[(0, 0), (0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5)])),
                ('comment', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at', 'pk'),
            },
        ),
        migrations.CreateModel(
            name='ImageForRestaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', utils.custom_imagefield.CustomImageField(blank=True, upload_to='restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptable_size_of_party', models.IntegerField(blank=True)),
                ('price', models.PositiveIntegerField(blank=True)),
                ('time', models.TimeField(choices=[(datetime.time(9, 0), '9시'), (datetime.time(10, 0), '10시'), (datetime.time(11, 0), '11시'), (datetime.time(12, 0), '12시'), (datetime.time(13, 0), '13시'), (datetime.time(14, 0), '14시'), (datetime.time(15, 0), '15시'), (datetime.time(16, 0), '16시'), (datetime.time(17, 0), '17시'), (datetime.time(18, 0), '18시'), (datetime.time(19, 0), '19시'), (datetime.time(20, 0), '20시'), (datetime.time(21, 0), '21시')])),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('strip_name', models.CharField(blank=True, max_length=20)),
                ('address', django_google_maps.fields.AddressField(max_length=200)),
                ('district', models.CharField(blank=True, max_length=20)),
                ('geolocation', django_google_maps.fields.GeoLocationField(max_length=100)),
                ('contact_number', models.CharField(max_length=11)),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('restaurant_type', models.CharField(choices=[('kor', 'Korean'), ('chn', 'Chinese'), ('jpn', 'Japanese'), ('mex', 'Mexican'), ('amc', 'American'), ('tha', 'Thai'), ('med', 'Mediterranean'), ('ita', 'Italian'), ('vtn', 'Vietnamese'), ('spn', 'Spanish'), ('ind', 'Indian'), ('etc', 'Etc')], max_length=3)),
                ('average_price', models.CharField(choices=[('c', 'Cheap'), ('n', 'Normal'), ('e', 'Expensive'), ('v', 'Very Expensive')], max_length=1)),
                ('thumbnail', utils.custom_imagefield.CustomImageField(blank=True, upload_to='thumbnail')),
                ('menu', utils.custom_imagefield.CustomImageField(blank=True, upload_to='menu')),
                ('business_hours', models.CharField(max_length=100)),
                ('star_rate', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=2)),
                ('maximum_party', models.PositiveIntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='reservationinfo',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_info', to='restaurants.Restaurant'),
        ),
        migrations.AddField(
            model_name='imageforrestaurant',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='restaurants.Restaurant'),
        ),
        migrations.AddField(
            model_name='comment',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='restaurants.Restaurant'),
        ),
    ]
