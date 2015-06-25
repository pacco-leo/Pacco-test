# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0036_auto_20150623_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watercategoriesvalue',
            name='value',
        ),
        migrations.RemoveField(
            model_name='watercategoriesvalue',
            name='valueType',
        ),
        migrations.AddField(
            model_name='watercategoriesvalue',
            name='valueMax',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='watercategoriesvalue',
            name='valueMin',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]
