# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-08 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timespan', models.CharField(max_length=20)),
                ('rating_text', models.TextField()),
                ('rating', models.CharField(max_length=20)),
            ],
        ),
    ]
