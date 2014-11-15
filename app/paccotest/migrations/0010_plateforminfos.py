# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0009_auto_20141115_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlateformInfos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('software_version', models.FloatField()),
                ('rpi_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
