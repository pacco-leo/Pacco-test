# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0026_calibrationsteps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='probe',
            name='id',
        ),
        migrations.AlterField(
            model_name='probe',
            name='channel',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
