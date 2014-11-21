# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0018_auto_20141118_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.CharField(default='text', max_length=300, verbose_name=b'text'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='text_en',
            field=models.CharField(max_length=300, null=True, verbose_name=b'text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text_fr',
            field=models.CharField(max_length=300, null=True, verbose_name=b'text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text_nl',
            field=models.CharField(max_length=300, null=True, verbose_name=b'text'),
        ),
    ]
