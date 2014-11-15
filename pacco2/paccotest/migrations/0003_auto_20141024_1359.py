# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0002_auto_20141023_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.AddField(
            model_name='answer',
            name='questions',
            field=models.ManyToManyField(to='paccotest.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='order_index',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
