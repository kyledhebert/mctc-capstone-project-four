# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-19 15:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0004_nprstory'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislator',
            name='saved_by_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
