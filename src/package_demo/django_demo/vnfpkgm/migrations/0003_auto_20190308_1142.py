# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2019-03-08 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vnfpkgm', '0002_auto_20190308_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='subscription_id',
            field=models.IntegerField(null=True),
        ),
    ]
