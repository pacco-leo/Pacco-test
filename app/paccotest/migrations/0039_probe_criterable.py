# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0038_auto_20150624_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='probe',
            name='criterable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
