# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0007_auto_20141109_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(default=0, to='paccotest.Question'),
            preserve_default=False,
        ),
    ]
