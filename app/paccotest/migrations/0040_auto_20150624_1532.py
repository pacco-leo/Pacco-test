# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0039_probe_criterable'),
    ]

    operations = [
        migrations.AddField(
            model_name='watercategorie',
            name='text_en',
            field=models.CharField(max_length=200, null=True, verbose_name=b'text'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='watercategorie',
            name='text_fr',
            field=models.CharField(max_length=200, null=True, verbose_name=b'text'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='watercategorie',
            name='text_nl',
            field=models.CharField(max_length=200, null=True, verbose_name=b'text'),
            preserve_default=True,
        ),
    ]
