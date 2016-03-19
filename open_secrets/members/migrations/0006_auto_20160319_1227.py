# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-19 17:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0005_legislator_saved_by_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedMemberDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_name', models.TextField()),
                ('contributors_list', models.TextField()),
                ('good_ratings_list', models.TextField()),
                ('bad_ratings_list', models.TextField()),
                ('npr_story_list', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='legislator',
            name='saved_by_users',
        ),
    ]
