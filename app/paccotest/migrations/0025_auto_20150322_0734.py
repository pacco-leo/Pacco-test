# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0024_auto_20150206_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probemeasure',
            name='measure',
            field=models.CharField(max_length=200, verbose_name=b'measure'),
        ),
        migrations.AlterField(
            model_name='question',
            name='actif',
            field=models.BooleanField(default=True),
        ),
    ]
