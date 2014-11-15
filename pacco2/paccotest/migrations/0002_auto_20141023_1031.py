# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='utc',
            field=models.DateTimeField(verbose_name=b'date'),
        ),
    ]
