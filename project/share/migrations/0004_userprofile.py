# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-19 11:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0003_auto_20160517_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realname', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='your birthday')),
                ('head', models.FileField(blank=True, upload_to='../upload/')),
                ('address', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
        ),
    ]