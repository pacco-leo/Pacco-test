# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0027_auto_20150504_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='probe',
            name='calibrable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
