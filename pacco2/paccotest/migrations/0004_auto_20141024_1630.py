# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0003_auto_20141024_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='questions',
        ),
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(to='paccotest.Answer'),
            preserve_default=True,
        ),
    ]
