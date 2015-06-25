# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0035_auto_20150623_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watercategoriesvalue',
            name='value',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
