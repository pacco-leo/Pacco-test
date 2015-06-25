# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0025_auto_20150322_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalibrationSteps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentence', models.CharField(max_length=300, verbose_name=b'sentence')),
                ('command', models.CharField(max_length=300, verbose_name=b'command')),
                ('delay', models.IntegerField()),
                ('tempCompensation', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
                ('probeType', models.ForeignKey(to='paccotest.Probe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
