# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LastUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_id', models.PositiveIntegerField()),
            ],
        ),
    ]
