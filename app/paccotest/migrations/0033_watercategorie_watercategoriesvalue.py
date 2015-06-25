# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0032_watercategories'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterCategorie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200, verbose_name=b'text')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaterCategoriesValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valueType', models.CharField(max_length=3, choices=[(1, b'max'), (0, b'min')])),
                ('value', models.IntegerField()),
                ('probeType', models.ForeignKey(to='paccotest.Probe')),
                ('waterCategorie', models.ForeignKey(to='paccotest.WaterCategorie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
