# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0021_answer_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='actif',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
