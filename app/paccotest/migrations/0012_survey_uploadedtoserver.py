# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0011_auto_20141115_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='uploadedToServer',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=True,
        ),
    ]
