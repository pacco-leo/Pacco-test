# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0030_auto_20150505_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calibrationmemo',
            name='date_calibration',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
