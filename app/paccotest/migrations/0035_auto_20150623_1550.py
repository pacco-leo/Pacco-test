# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0034_auto_20150623_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watercategoriesvalue',
            name='valueType',
            field=models.CharField(max_length=1, choices=[(b'1', b'max'), (b'0', b'min')]),
        ),
    ]
