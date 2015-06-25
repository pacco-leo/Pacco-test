# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0029_calibrationmemo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calibrationmemo',
            name='probeType',
            field=models.ForeignKey(to='paccotest.Probe', unique=True),
        ),
    ]
