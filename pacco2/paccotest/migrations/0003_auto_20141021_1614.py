# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0002_auto_20141021_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useranswer',
            old_name='userAnswer',
            new_name='answer',
        ),
    ]
