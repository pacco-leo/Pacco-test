# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0040_auto_20150624_1532'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WaterCategories',
        ),
        migrations.AddField(
            model_name='watercategorie',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
