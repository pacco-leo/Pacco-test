# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0028_probe_calibrable'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalibrationMemo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_calibration', models.DateTimeField()),
                ('probeType', models.ForeignKey(to='paccotest.Probe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
