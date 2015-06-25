# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0031_auto_20150505_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200, verbose_name=b'text')),
                ('phMax', models.CharField(max_length=200, verbose_name=b'phMax')),
                ('phMin', models.CharField(max_length=200, verbose_name=b'phMin')),
                ('ecMax', models.CharField(max_length=200, verbose_name=b'ecMax')),
                ('ecMin', models.CharField(max_length=200, verbose_name=b'ecMin')),
                ('doMax', models.CharField(max_length=200, verbose_name=b'doMax')),
                ('doMin', models.CharField(max_length=200, verbose_name=b'doMin')),
                ('orpMax', models.CharField(max_length=200, verbose_name=b'orpMax')),
                ('orpMin', models.CharField(max_length=200, verbose_name=b'orpMin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
