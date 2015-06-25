# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0033_watercategorie_watercategoriesvalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watercategoriesvalue',
            name='valueType',
            field=models.CharField(max_length=1, choices=[(1, b'max'), (0, b'min')]),
        ),
    ]
