# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2019-02-07 02:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctim', '0003_auto_20180208_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='demo_dashboard_base_date',
        ),
        migrations.RemoveField(
            model_name='config',
            name='demo_enable',
        ),
    ]