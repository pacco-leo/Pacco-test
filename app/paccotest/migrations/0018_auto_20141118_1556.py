# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0017_auto_20141118_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text_en',
            field=models.CharField(max_length=300, verbose_name=b'text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text_fr',
            field=models.CharField(max_length=300, verbose_name=b'text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text_nl',
            field=models.CharField(max_length=300, verbose_name=b'text'),
        ),
    ]
