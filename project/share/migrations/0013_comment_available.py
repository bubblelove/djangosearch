# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-26 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0012_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
